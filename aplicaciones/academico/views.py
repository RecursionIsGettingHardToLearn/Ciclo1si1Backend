from rest_framework import viewsets
from .models import Grado, Paralelo, Curso, Materia, MateriaCurso
from .serializers import (
    GradoSerializer,
    ParaleloSerializer,
    CursoSerializer,
    MateriaSerializer,
    MateriaCursoSerializer
)

class GradoViewSet(viewsets.ModelViewSet):
    queryset = Grado.objects.all()
    serializer_class = GradoSerializer
    filterset_fields = ['unidad_educativa', 'nivel_educativo']

class ParaleloViewSet(viewsets.ModelViewSet):
    queryset = Paralelo.objects.all()
    serializer_class = ParaleloSerializer
    filterset_fields = ['grado', 'letra']

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filterset_fields = ['paralelo']

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    filterset_fields = ['nombre']
    search_fields = ['nombre']

class MateriaCursoViewSet(viewsets.ModelViewSet):
    queryset = MateriaCurso.objects.all()
    serializer_class = MateriaCursoSerializer
    filterset_fields = ['curso', 'materia']