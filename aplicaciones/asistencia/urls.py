from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'comportamientos', views.ComportamientoViewSet)
router.register(r'licencias', views.LicenciaViewSet)
router.register(r'asistencias-generales', views.AsistenciaGeneralViewSet)
router.register(r'asistencias-clases', views.AsistenciaClaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]