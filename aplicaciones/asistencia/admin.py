from django.contrib import admin
from .models import (
    Comportamiento,
    Licencia,
    AsistenciaGeneral,
    AsistenciaClase
)

@admin.register(Comportamiento)
class ComportamientoAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha', 'tipo', 'gravedad')
    list_filter = ('tipo', 'gravedad', 'fecha')
    search_fields = ('estudiante__usuario__nombre', 'descripcion')
    date_hierarchy = 'fecha'

@admin.register(Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_inicio')
    search_fields = ('estudiante__usuario__nombre', 'motivo')
    date_hierarchy = 'fecha_inicio'

@admin.register(AsistenciaGeneral)
class AsistenciaGeneralAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha', 'estado', 'hora_entrada', 'hora_salida')
    list_filter = ('estado', 'fecha')
    search_fields = ('estudiante__usuario__nombre',)
    date_hierarchy = 'fecha'

@admin.register(AsistenciaClase)
class AsistenciaClaseAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'clase', 'fecha', 'estado')
    list_filter = ('clase', 'estado', 'fecha')
    search_fields = ('estudiante__usuario__nombre',)
    date_hierarchy = 'fecha'