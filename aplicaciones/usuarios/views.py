from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token 
from rest_framework.response import Response

from usuarios.models import Usuario
from .serializer import (
    UsuarioSerializer,
    UsuarioCreateSerializer,
)


class UsuarioListView(generics.ListAPIView):
    """
    Lista todos los usuarios (solo autenticados).
    """
    queryset = Usuario.objects.select_related("rol").all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class UsuarioCreateView(generics.CreateAPIView):
    """
    Crea un usuario (solo admins / superusers).
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioCreateSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]


class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar un usuario específico.
    """
    queryset = Usuario.objects.select_related("rol").all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CustomAuthToken(ObtainAuthToken):
    """
    Devuelve token + info básica del usuario (rol, nombre completo).
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)   # valida credenciales
        token = Token.objects.get(key=response.data["token"])
        user = token.user
        return Response({
            "token": token.key,
            "username": user.username,
            "rol": user.rol.nombre,
            "full_name": user.get_full_name(),
        })


# api/views/login_views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from django.contrib.auth import authenticate


from usuarios.models import Usuario, Bitacora


@csrf_exempt       # si usas DRF ViewSet, no es necesario
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"detail": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if not user:
            return JsonResponse({"success": False, "message": "Credenciales incorrectas"}, status=401)

        if not user.is_active:
            return JsonResponse({"success": False, "message": "Cuenta inactiva"}, status=403)
        print("HI")

        # Token (crea si no existe)
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        print("TATA")
        # Registrar entrada en Bitácora
        Bitacora.objects.create(usuario=user, hora_entrada=timezone.now())

        print("Hellow")

        return JsonResponse({
            "success": True,
            "token": token.key,
            "username": user.username,
            "rol": user.rol.nombre,
        })

    except Exception as e:
        print(f"Error en login_view: {e}")
        return JsonResponse({"success": False, "message": f"Error interno: {e}"}, status=500)
