from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'estudiantes', views.EstudianteViewSet)
router.register(r'tutores', views.TutorViewSet)
router.register(r'relaciones', views.TutorEstudianteViewSet, basename='tutor-estudiante')

urlpatterns = [
    path('', include(router.urls)),
]