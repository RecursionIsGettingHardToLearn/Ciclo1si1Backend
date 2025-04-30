from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.usuario_views import (
    UsuarioViewSet,
    RolViewSet,
    NotificacionViewSet,
    BitacoraViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'roles', RolViewSet, basename='rol')
router.register(r'notificaciones', NotificacionViewSet, basename='notificacion')
router.register(r'bitacoras', BitacoraViewSet, basename='bitacora')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include([
        path('login/', UsuarioViewSet.as_view({'post': 'login'}), name='login'),
        path('logout/', UsuarioViewSet.as_view({'post': 'logout'}), name='logout'),
        path('register/', UsuarioViewSet.as_view({'post': 'register'}), name='register'),
    ])),
]