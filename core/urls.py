
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from django.http import HttpResponse



urlpatterns = [
    path('admin/', admin.site.urls),
    path("usuarios/", include("aplicaciones.usuarios.urls")),
    path("", lambda request: HttpResponse("¡Hola desde Django en Render!")),
    
]
