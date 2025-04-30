from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'grados', views.GradoViewSet)
router.register(r'paralelos', views.ParaleloViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'materias', views.MateriaViewSet)
router.register(r'materias-curso', views.MateriaCursoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]