from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'dimensiones', views.DimensionEvaluacionViewSet)
router.register(r'actividades', views.ActividadViewSet)
router.register(r'notas-actividades', views.NotaActividadViewSet)
router.register(r'notas-finales', views.NotaFinalMateriaViewSet)
router.register(r'auto-evaluaciones', views.AutoEvaluacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]