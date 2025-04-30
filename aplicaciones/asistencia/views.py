from rest_framework import viewsets, filters
from .models import (
    Comportamiento,
    Licencia,
    AsistenciaGeneral,
    AsistenciaClase
)
from .serializers import (
    ComportamientoSerializer,
    LicenciaSerializer,
    AsistenciaGeneralSerializer,
    AsistenciaClaseSerializer,
    CreateComportamientoSerializer,
    CreateLicenciaSerializer,
    CreateAsistenciaGeneralSerializer,
    CreateAsistenciaClaseSerializer
)

class ComportamientoViewSet(viewsets.ModelViewSet):
    queryset = Comportamiento.objects.all()
    filterset_fields = ['estudiante', 'tipo', 'fecha']
    search_fields = ['descripcion']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateComportamientoSerializer
        return ComportamientoSerializer

class LicenciaViewSet(viewsets.ModelViewSet):
    queryset = Licencia.objects.all()
    filterset_fields = ['estudiante', 'tutor', 'estado']
    search_fields = ['motivo']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateLicenciaSerializer
        return LicenciaSerializer

class AsistenciaGeneralViewSet(viewsets.ModelViewSet):
    queryset = AsistenciaGeneral.objects.all()
    filterset_fields = ['estudiante', 'estado', 'fecha']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateAsistenciaGeneralSerializer
        return AsistenciaGeneralSerializer

class AsistenciaClaseViewSet(viewsets.ModelViewSet):
    queryset = AsistenciaClase.objects.all()
    filterset_fields = ['clase', 'estudiante', 'estado', 'fecha']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateAsistenciaClaseSerializer
        return AsistenciaClaseSerializer