from rest_framework import viewsets
from .models import Colegio, Modulo, Aula, UnidadEducativa
from .serializers import (
    ColegioSerializer,
    ModuloSerializer,
    AulaSerializer,
    UnidadEducativaSerializer,
    CreateColegioSerializer,
    CreateModuloSerializer,
    CreateAulaSerializer,
    CreateUnidadEducativaSerializer
)

class ColegioViewSet(viewsets.ModelViewSet):
    queryset = Colegio.objects.all()
    search_fields = ['nombre', 'direccion']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateColegioSerializer
        return ColegioSerializer

class ModuloViewSet(viewsets.ModelViewSet):
    queryset = Modulo.objects.all()
    search_fields = ['nombre']
    filterset_fields = ['cantidad_aulas']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateModuloSerializer
        return ModuloSerializer

class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    filterset_fields = ['modulo', 'tipo', 'estado']
    search_fields = ['nombre', 'equipamiento']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateAulaSerializer
        return AulaSerializer

class UnidadEducativaViewSet(viewsets.ModelViewSet):
    queryset = UnidadEducativa.objects.all()
    filterset_fields = ['colegio', 'turno']
    search_fields = ['codigo_sie', 'direccion']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateUnidadEducativaSerializer
        return UnidadEducativaSerializer