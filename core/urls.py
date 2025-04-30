from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
urlpatterns = [
     path('admin/', admin.site.urls),  
    path("user/", include("aplicaciones.usuarios.urls")),  
    path('', TemplateView.as_view(template_name='index.html')),  # Para servir React
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
