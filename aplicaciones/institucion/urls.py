from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'colegios', views.ColegioViewSet)
router.register(r'modulos', views.ModuloViewSet)
router.register(r'aulas', views.AulaViewSet)
router.register(r'unidades-educativas', views.UnidadEducativaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]