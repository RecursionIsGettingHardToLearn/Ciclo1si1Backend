from rest_framework import serializers
from .models import (
    Comportamiento,
    Licencia,
    AsistenciaGeneral,
    AsistenciaClase
)
from estudiantes.serializers import EstudianteSerializer, TutorSerializer
from academico.serializers import ClaseSerializer

class ComportamientoSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer()
    
    class Meta:
        model = Comportamiento
        fields = '__all__'

class LicenciaSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer()
    tutor = TutorSerializer()
    
    class Meta:
        model = Licencia
        fields = '__all__'

class AsistenciaGeneralSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer()
    
    class Meta:
        model = AsistenciaGeneral
        fields = '__all__'

class AsistenciaClaseSerializer(serializers.ModelSerializer):
    clase = ClaseSerializer()
    estudiante = EstudianteSerializer()
    licencia = LicenciaSerializer()
    
    class Meta:
        model = AsistenciaClase
        fields = '__all__'

# Serializers para creación/actualización
class CreateComportamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comportamiento
        fields = '__all__'

class CreateLicenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licencia
        fields = '__all__'

class CreateAsistenciaGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenciaGeneral
        fields = '__all__'

class CreateAsistenciaClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenciaClase
        fields = '__all__'