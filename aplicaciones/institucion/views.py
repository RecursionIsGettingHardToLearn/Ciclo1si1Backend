from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import OuterRef, Subquery
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Colegio, Modulo, Aula, UnidadEducativa,SuperAdmin
from usuarios.utils import registrar_bitacora
from usuarios.usuario_views import get_client_ip 
from .serializers import (
    ColegioSerializer,
    ModuloSerializer,
    AulaSerializer,
    UnidadEducativaSerializer,
    CreateColegioSerializer,
    CreateModuloSerializer,
    CreateAulaSerializer,
    CreateUnidadEducativaSerializer
)

class ColegioViewSet(viewsets.ModelViewSet):
    queryset = Colegio.objects.all()
    search_fields = ['nombre', 'direccion']
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateColegioSerializer
        return ColegioSerializer

    @action(detail=False, methods=['get'], url_path='cantidad')
    def obtener_cantidad_colegios(self, request):
        cantidad = Colegio.objects.count()
        registrar_bitacora(
            usuario=request.user,
            ip=get_client_ip(request),
            tabla='colegio',
            accion='ver',
            descripcion='Consultó la cantidad de colegios'
        )
        return Response({'cantidad_colegios': cantidad})

    @action(detail=False, methods=['post'], url_path='crear')
    def crear_colegio(self, request):
        """
        Endpoint to create a Colegio with the specified fields.
       """
        data = request.data.copy()

        usuario_id = data.get('usuario_id')
        if usuario_id:
            superadmin = SuperAdmin.objects.filter(usuario_id=usuario_id).first()
            if not superadmin:
                return Response({'error': 'SuperAdmin no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
            data['super_admin_fk'] = superadmin.usuario_id
            data.pop('usuario_id', None)  # eliminar si no lo necesitas más

        serializer = CreateColegioSerializer(data=data, context={"request": request})
        print("serializer", serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='colegio',
                accion='crear',
                descripcion=f'Creó el colegio nuevo'
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True, methods=['delete'], url_path='eliminar')
    def eliminar_colegio(self, request, pk=None):
        """
        Endpoint to delete a Colegio by its ID.
        """
        try:
            colegio = Colegio.objects.get(pk=pk)
            colegio.delete()
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='colegio',
                accion='eliminar',
                descripcion=f'Eliminó el colegio )'
            )
            return Response({'detail': 'Colegio eliminado exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
        except Colegio.DoesNotExist:
            return Response({'detail': 'Colegio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'], url_path='editar')
    def editar_colegio(self, request, pk=None):
        """
        Endpoint to edit a Colegio by its ID.
        """
        try:
            colegio = Colegio.objects.get(pk=pk)
            serializer = CreateColegioSerializer(colegio, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                registrar_bitacora(
                    usuario=request.user,
                    ip=get_client_ip(request),
                    tabla='colegio',
                    accion='editar',
                    descripcion=f'Editó el colegio '
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Colegio.DoesNotExist:
            return Response({'detail': 'Colegio no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='listar')
    def listar_colegios(self, request):
        """
        Endpoint to list all Colegios.
        """
        colegios = Colegio.objects.all()
        serializer = ColegioSerializer(colegios, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='listar-colegios-unidades-educativas')
    def listar_colegios_unidades_educativas(self, request):
        data = Colegio.objects.filter(
            unidades_educativas__isnull=False  # Solo colegios con unidades educativas asociadas
        ).values('nombre', 'unidades_educativas__id')  # Obtener el nombre del colegio y el ID de la unidad educativa
        registrar_bitacora(
            usuario=request.user,
            ip=get_client_ip(request),
            tabla='colegio',
            accion='ver',
            descripcion='Listó colegios con unidades educativas asociadas'
        )
        return Response(data, status=status.HTTP_200_OK)

class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    search_fields = ['nombre']
    filterset_fields = ['cantidad_aulas']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateModuloSerializer
        return ModuloSerializer

    @action(detail=False, methods=['get'])
    def listar_modulos(self, request):
        modulos = self.get_queryset()
        serializer = self.get_serializer(modulos, many=True)
        
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def crear_modulo(self, request):
        serializer = self.get_serializer(data=request.data)
        print("serializer", serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='modulo',
                accion='crear',
                descripcion=f'Creó el módulo nuevo'
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def editar_modulo(self, request, pk=None):
        try:
            modulo = Modulo.objects.get(pk=pk)
        except Modulo.DoesNotExist:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(modulo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='modulo',
                accion='editar',
                descripcion=f'Editó el módulo '
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def eliminar_modulo(self, request, pk=None):
        try:
            modulo = Modulo.objects.get(pk=pk)
        except Modulo.DoesNotExist:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        modulo.delete()
        registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='modulo',
                accion='eliminar',
                descripcion=f'Eliminó el módulo )'
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    filterset_fields = ['modulo', 'tipo', 'estado']
    search_fields = ['nombre', 'equipamiento']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateAulaSerializer
        return AulaSerializer

    @action(detail=False, methods=['get'])
    def listar_aulas(self, request):
        aulas = Aula.objects.all()
        serializer = AulaSerializer(aulas, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def crear_aula(self, request):
        serializer = AulaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='aula',
                accion='crear',
                descripcion=f'Creó el aula'
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def editar_aula(self, request, pk=None):
        try:
            aula = Aula.objects.get(pk=pk)
        except Aula.DoesNotExist:
            return Response({'detail': 'Aula no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AulaSerializer(aula, data=request.data)
        if serializer.is_valid():
            serializer.save()
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='aula',
                accion='editar',
                descripcion=f'Editó el aula )'
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def eliminar_aula(self, request, pk=None):
        try:
            aula = Aula.objects.get(pk=pk)
        except Aula.DoesNotExist:
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='aula',
                accion='eliminar',
                descripcion=f'Eliminó el aula '
            )
            return Response({'detail': 'Aula no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        aula.delete()
        return Response({'detail': 'Aula eliminada'}, status=status.HTTP_204_NO_CONTENT)

class UnidadEducativaViewSet(viewsets.ModelViewSet):
    queryset = UnidadEducativa.objects.all()
    filterset_fields = ['colegio', 'turno']
    search_fields = ['codigo_sie', 'direccion']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateUnidadEducativaSerializer
        return UnidadEducativaSerializer

    @action(detail=False, methods=['get'], url_path='cantidad')
    def obtener_cantidad_unidades_educativas(self, request):
        cantidad = UnidadEducativa.objects.count()
        registrar_bitacora(
            usuario=request.user,
            ip=get_client_ip(request),
            tabla='unidad_educativa',
            accion='ver',
            descripcion='Consultó la cantidad de unidades educativas'
        )
        return Response({'cantidad_unidades_educativas': cantidad})
    
    @action(detail=False, methods=['post'], url_path='crear')
    def crear_unidad_educativa(self, request):
        serializer = CreateUnidadEducativaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            registrar_bitacora(
            usuario=request.user,
            ip=get_client_ip(request),
            tabla='unidad_educativa',
            accion='crear',
            descripcion='Creó una nueva unidad educativa'
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'], url_path='editar')
    def editar_unidad_educativa(self, request, pk=None):
        try:

            unidad = UnidadEducativa.objects.get(pk=pk)
        except UnidadEducativa.DoesNotExist:
            return Response({'detail': 'Unidad Educativa no encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreateUnidadEducativaSerializer(unidad, data=request.data)
        print("serializer",serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='unidad_educativa',
                accion='editar',
                descripcion=f'Editó la unidad educativa con ID: '
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'], url_path='eliminar')
    def eliminar_unidad_educativa(self, request, pk=None):
        try:
            unidad = UnidadEducativa.objects.get(pk=pk)
            unidad.delete()
            registrar_bitacora(
                usuario=request.user,
                ip=get_client_ip(request),
                tabla='unidad_educativa',
                accion='eliminar',
                descripcion=f'Eliminó la unidad educativa con código SIE:'
            )
            return Response({'detail': 'Unidad Educativa eliminada exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
        except UnidadEducativa.DoesNotExist:
            return Response({'detail': 'Unidad Educativa no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], url_path='listar')
    def listar_unidades_educativas(self, request):
        unidades = UnidadEducativa.objects.all()
        serializer = UnidadEducativaSerializer(unidades, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

