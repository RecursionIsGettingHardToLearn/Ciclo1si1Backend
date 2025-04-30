from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Profesor, Especialidad, ProfesorEspecialidad
from .serializers import (
    ProfesorSerializer,
    EspecialidadSerializer,
    ProfesorEspecialidadSerializer,
    CreateProfesorSerializer,
    CreateProfesorEspecialidadSerializer
)

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    filterset_fields = ['estado']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateProfesorSerializer
        return ProfesorSerializer
    
    @action(detail=True, methods=['get'])
    def especialidades(self, request, pk=None):
        profesor = self.get_object()
        especialidades = profesor.especialidades.all()
        serializer = ProfesorEspecialidadSerializer(especialidades, many=True)
        return Response(serializer.data)

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    filterset_fields = ['materia']
    search_fields = ['nombre']

class ProfesorEspecialidadViewSet(viewsets.ModelViewSet):
    queryset = ProfesorEspecialidad.objects.all()
    serializer_class = ProfesorEspecialidadSerializer
    filterset_fields = ['profesor', 'especialidad']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateProfesorEspecialidadSerializer
        return ProfesorEspecialidadSerializer