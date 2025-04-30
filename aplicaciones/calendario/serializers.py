from rest_framework import serializers
from .models import (
    CalendarioAcademico,
    Periodo,
    TipoFeriado,
    Feriado,
    TipoHorario,
    Horario,
    ClaseHorario
)
from institucion.serializers import UnidadEducativaSerializer

class CalendarioAcademicoSerializer(serializers.ModelSerializer):
    unidad_educativa = UnidadEducativaSerializer()
    
    class Meta:
        model = CalendarioAcademico
        fields = '__all__'

class PeriodoSerializer(serializers.ModelSerializer):
    calendario = CalendarioAcademicoSerializer()
    
    class Meta:
        model = Periodo
        fields = '__all__'

class TipoFeriadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoFeriado
        fields = '__all__'

class FeriadoSerializer(serializers.ModelSerializer):
    calendario = CalendarioAcademicoSerializer()
    tipo = TipoFeriadoSerializer()
    
    class Meta:
        model = Feriado
        fields = '__all__'

class TipoHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoHorario
        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    tipo = TipoHorarioSerializer()
    
    class Meta:
        model = Horario
        fields = '__all__'

class ClaseHorarioSerializer(serializers.ModelSerializer):
    clase = serializers.StringRelatedField()
    horario = HorarioSerializer()
    
    class Meta:
        model = ClaseHorario
        fields = '__all__'

# Serializers para creación/actualización
class CreateCalendarioAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarioAcademico
        fields = '__all__'

class CreatePeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = '__all__'

class CreateFeriadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feriado
        fields = '__all__'

class CreateHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class CreateClaseHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaseHorario
        fields = '__all__'