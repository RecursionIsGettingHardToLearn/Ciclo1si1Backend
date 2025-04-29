from rest_framework import serializers
from .models import (
    Rol,
    Usuario,
    Notificacion,
    SuperAdmin,
    Admin,
    Bitacora
)
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'id',
            'ci',
            'foto',
            'nombre',
            'apellido',
            'email',
            'edad',
            'username',
            'estado',
            'rol',
            'telefono',
            'is_staff',
            'is_active',
            'date_joined'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UsuarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'ci',
            'nombre',
            'apellido',
            'email',
            'username',
            'password',
            'rol',
            'telefono'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            ci=validated_data['ci'],
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            username=validated_data['username'],
            password=validated_data['password'],
            rol=validated_data.get('rol'),
            telefono=validated_data.get('telefono')
        )
        return user

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                              username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class NotificacionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Notificacion
        fields = '__all__'

class NotificacionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['usuario', 'titulo', 'mensaje', 'tipo']

class SuperAdminSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = SuperAdmin
        fields = '__all__'

class SuperAdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['usuario']

class AdminSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Admin
        fields = '__all__'

class AdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['usuario', 'puesto']

class BitacoraSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = Bitacora
        fields = '__all__'

class BitacoraCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = ['usuario', 'hora_entrada']

class BitacoraUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = ['hora_salida']