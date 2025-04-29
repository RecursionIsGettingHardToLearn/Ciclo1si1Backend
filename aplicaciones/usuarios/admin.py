from django.contrib import admin
from .models import Rol, Usuario, SuperAdmin, Admin, Bitacora

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username','nombre','apellido','email','rol','is_staff','is_active')
    list_filter  = ('rol','is_staff','is_active')

@admin.register(SuperAdmin)
class SuperAdminAdmin(admin.ModelAdmin):
    list_display = ('usuario',)

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('usuario','puesto','estado')

@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display = ('usuario','hora_entrada','hora_salida')
