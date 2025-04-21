
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls'))
]
