from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .models import Usuario, Rol, Notificacion, Bitacora,SuperAdmin
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.mail import send_mail
from random import randint
from rest_framework.views import APIView
from .serializer import (

    UsuarioSerializer,
    RolSerializer,
    NotificacionSerializer,
    BitacoraSerializer,
    LoginSerializer,
    SuperAdminSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from rest_framework.decorators import permission_classes
from usuarios.utils import registrar_bitacora

@permission_classes([AllowAny])
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAdminUser]

    def register(self, request):
        print("inteto de registro")
        serializer = self.get_serializer(data=request.data)
        print("Datos iniciales enviados al serializador:", serializer.initial_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response({
            'user': serializer.data,
            'message': 'Usuario registrado exitosamente'
        }, status=status.HTTP_201_CREATED)




    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'error': 'Cuenta desactivada'}, status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=user)
        ip = get_client_ip(request)

        registrar_bitacora(
            usuario=user,
            ip=ip,
            tabla='usuario',
            accion='crear',
            descripcion='Inicio de sesión exitoso'
        )

        return Response({
            'token': token.key,
            'user': UsuarioSerializer(user).data
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        bitacora = Bitacora.objects.filter(
            usuario=request.user,
            hora_salida__isnull=True
        ).last()

        if bitacora:
            bitacora.hora_salida = timezone.now()
            bitacora.descripcion = "Cierre de sesión"
            bitacora.save()
        else:
        # Opción: registrar nuevo solo si no se encontró uno anterior
            ip = get_client_ip(request)
            Bitacora.objects.create(
                usuario=request.user,
                hora_entrada=timezone.now(),
                hora_salida=timezone.now(),
                ip=ip,
                tabla="usuario",
                accion="ver",
                descripcion="Cierre de sesión sin entrada previa"
            )

        request.user.auth_token.delete()
        logout(request)

        return Response({'message': 'Sesión cerrada correctamente'})
    
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def cantidad(self, request):
        cantidad = Usuario.objects.count()

        return Response({'cantidad_usuarios': cantidad})
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def perfil(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)



    @action(detail=False, methods=['get'], url_path='listar-usuarios')
    def listar_usuarios(self, request):
    # Aquí NO uses self.get_object()
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        registrar_bitacora(
        usuario=request.user,
        ip=get_client_ip(request),
        tabla='usuario',
        accion='ver',
        descripcion='Listó los usuarios'
    )
        return Response(serializer.data)
   
    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAdminUser])
    def editar_usuario(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(usuario, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Guardar cambios normales primero (sin aplicar password)
        usuario = serializer.save()

    # Si se quiere cambiar la contraseña
        nueva_contraseña = request.data.get("password")
        if nueva_contraseña:
            usuario.set_password(nueva_contraseña)
            usuario.save()

        registrar_bitacora(
            usuario=request.user,
            ip=get_client_ip(request),
            tabla='usuario',
            accion='editar',
            descripcion=f'Editó el usuario con ID {pk}'
        )

        return Response({
            'usuario': serializer.data,
            'message': 'Usuario actualizado exitosamente'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAdminUser])
    def eliminar_usuario(self, request, pk=None):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
        usuario.delete()
        registrar_bitacora(
        usuario=request.user,
        ip=get_client_ip(request),
        tabla='usuario',
        accion='eliminar',
        descripcion=f'Eliminó un usuario  '
    )
    
        return Response({'message': 'Usuario eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='listar-superadmins', permission_classes=[permissions.IsAdminUser])
    def listar_superadmins(self, request):
        queryset = SuperAdmin.objects.select_related('usuario').all()
        serializer = SuperAdminSerializer(queryset, many=True)
        
        return Response(serializer.data)

    

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [permissions.IsAdminUser]

class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        notificacion = self.get_object()
        notificacion.leida = True
        notificacion.save()
        return Response({'status': 'notificación marcada como leída'})

class BitacoraViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BitacoraSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Bitacora.objects.all().order_by('-hora_entrada')


def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
