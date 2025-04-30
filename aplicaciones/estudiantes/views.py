from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Estudiante, Tutor, TutorEstudiante
from .serializers import (
    EstudianteSerializer,
    TutorSerializer,
    TutorEstudianteSerializer,
    CreateEstudianteSerializer,
    CreateTutorSerializer,
    CreateTutorEstudianteSerializer
)

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    filterset_fields = ['estado', 'curso']
    search_fields = ['usuario__nombre', 'usuario__apellido', 'rude']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateEstudianteSerializer
        return EstudianteSerializer
    
    @action(detail=True, methods=['get'])
    def tutores(self, request, pk=None):
        estudiante = self.get_object()
        tutores = estudiante.tutores.all()
        serializer = TutorEstudianteSerializer(tutores, many=True)
        return Response(serializer.data)

class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    filterset_fields = ['parentesco']
    search_fields = ['usuario__nombre', 'usuario__apellido']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateTutorSerializer
        return TutorSerializer
    
    @action(detail=True, methods=['get'])
    def estudiantes(self, request, pk=None):
        tutor = self.get_object()
        estudiantes = tutor.estudiantes.all()
        serializer = TutorEstudianteSerializer(estudiantes, many=True)
        return Response(serializer.data)

class TutorEstudianteViewSet(viewsets.ModelViewSet):
    queryset = TutorEstudiante.objects.all()
    serializer_class = TutorEstudianteSerializer
    filterset_fields = ['tutor', 'estudiante', 'es_principal']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateTutorEstudianteSerializer
        return TutorEstudianteSerializer