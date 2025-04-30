from rest_framework import serializers
from .models import Profesor, Especialidad, ProfesorEspecialidad
from usuarios.serializer import UsuarioSerializer  # Asegúrate de tener este serializer
from academico.serializers import MateriaSerializer

class EspecialidadSerializer(serializers.ModelSerializer):
    materia = MateriaSerializer()
    
    class Meta:
        model = Especialidad
        fields = '__all__'

class ProfesorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    
    class Meta:
        model = Profesor
        fields = '__all__'

class ProfesorEspecialidadSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer()
    especialidad = EspecialidadSerializer()
    
    class Meta:
        model = ProfesorEspecialidad
        fields = '__all__'

# Serializers para creación/actualización
class CreateProfesorEspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesorEspecialidad
        fields = ['profesor', 'especialidad']

class CreateProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = ['usuario', 'estado']