from rest_framework import serializers
from .models import Colegio, Modulo, Aula, UnidadEducativa

class ColegioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colegio
        fields = '__all__'

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'

class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__'

class UnidadEducativaSerializer(serializers.ModelSerializer):
    colegio = ColegioSerializer()
    
    class Meta:
        model = UnidadEducativa
        fields = '__all__'

# Serializers para creación/actualización
class CreateColegioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colegio
        fields = '__all__'

class CreateModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'

class CreateAulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__'

class CreateUnidadEducativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadEducativa
        fields = '__all__'