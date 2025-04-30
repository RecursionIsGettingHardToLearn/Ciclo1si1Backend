from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'calendarios', views.CalendarioAcademicoViewSet)
router.register(r'periodos', views.PeriodoViewSet)
router.register(r'tipos-feriado', views.TipoFeriadoViewSet)
router.register(r'feriados', views.FeriadoViewSet)
router.register(r'tipos-horario', views.TipoHorarioViewSet)
router.register(r'horarios', views.HorarioViewSet)
router.register(r'clase-horarios', views.ClaseHorarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]