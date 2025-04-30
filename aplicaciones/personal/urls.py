from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profesores', views.ProfesorViewSet)
router.register(r'especialidades', views.EspecialidadViewSet)
router.register(r'asignaciones', views.ProfesorEspecialidadViewSet, basename='profesor-especialidad')

urlpatterns = [
    path('', include(router.urls)),
]