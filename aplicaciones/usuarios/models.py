from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'usuarios'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        db_table = 'rol'

    def __str__(self):
        return self.nombre

class UsuarioManager(BaseUserManager):
    def create_user(self, ci, email, nombre, apellido, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        if not ci:
            raise ValueError('El CI es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(
            ci=ci,
            email=email,
            nombre=nombre,
            apellido=apellido,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ci, email, nombre, apellido, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Obtener o crear rol de SuperAdmin
        rol, _ = Rol.objects.get_or_create(nombre='SuperAdmin')
        extra_fields.setdefault('rol', rol)
        
        return self.create_user(ci, email, nombre, apellido, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    ci = models.CharField(max_length=20, unique=True)
    foto = models.ImageField(upload_to='usuarios/fotos/', blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)  # Reemplazo de edad
    username = models.CharField(max_length=50, unique=True)
    estado = models.BooleanField(default=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    password_reset_pin = models.CharField(max_length=6, blank=True, null=True)
    
    # Campos requeridos para el modelo de usuario personalizado
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['ci', 'email', 'nombre', 'apellido', 'fecha_nacimiento']  # Actualización de campos requeridos

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"

    def get_short_name(self):
        return self.nombre

class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        db_table = 'notificacion'
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.titulo} - {self.usuario}"

class SuperAdmin(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='superadmin'
    )
    

    class Meta:
        verbose_name = 'Super Administrador'
        verbose_name_plural = 'Super Administraadores'
        db_table = 'superadmin'

    def __str__(self):
        return str(self.usuario)

class Admin(models.Model):
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='admin'
    )
    puesto = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
        db_table = 'admin'

    def __str__(self):
        return f"{self.usuario} - {self.puesto}"
# Create your models here.
class Bitacora(models.Model):
    ACCIONES = [
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('eliminar', 'Eliminar'),
        ('ver', 'Ver'),
        ('otro', 'Otro'),
    ]
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario'
    )
    hora_entrada = models.DateTimeField(verbose_name='Hora de entrada')
    hora_salida = models.DateTimeField(
        verbose_name='Hora de salida',
        blank=True,
        null=True
    )
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")
    tabla = models.CharField(max_length=100, verbose_name='Tabla afectada')
    accion = models.CharField(max_length=10, choices=ACCIONES)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'Bitácora de sesión'
        verbose_name_plural = 'Bitácoras de sesión'
        db_table = 'bitacora_sesion'
        ordering = ['-hora_entrada']

    def __str__(self):
        return f"{self.usuario} entró {self.hora_entrada:%Y-%m-%d %H:%M:%S}"
