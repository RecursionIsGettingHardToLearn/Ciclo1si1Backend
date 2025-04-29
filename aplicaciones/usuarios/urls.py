from django.urls import path
from usuarios.views import (
    UsuarioListView, UsuarioCreateView, UsuarioDetailView, CustomAuthToken, login_view
)


urlpatterns = [
    # Auth
    path("token/", CustomAuthToken.as_view(), name="api-token"),
    path("login/", login_view, name="login"),

    # Usuarios
    path("", UsuarioListView.as_view(), name="usuario-list"),
    path("crear/", UsuarioCreateView.as_view(), name="usuario-create"),
    path("<int:pk>/", UsuarioDetailView.as_view(), name="usuario-detail"),
]
