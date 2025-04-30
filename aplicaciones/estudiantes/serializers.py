from rest_framework import serializers
from .models import Estudiante, Tutor, TutorEstudiante
from usuarios.serializer import UsuarioSerializer
from academico.serializers import CursoSerializer

class EstudianteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    curso = CursoSerializer()
    
    class Meta:
        model = Estudiante
        fields = '__all__'

class TutorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Tutor
        fields = '__all__'

class TutorEstudianteSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer()
    estudiante = EstudianteSerializer()
    
    class Meta:
        model = TutorEstudiante
        fields = '__all__'

# Serializers para creación/actualización
class CreateEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ['usuario', 'rude', 'estado', 'curso']

class CreateTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['usuario', 'parentesco']

class CreateTutorEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorEstudiante
        fields = ['tutor', 'estudiante', 'es_principal']