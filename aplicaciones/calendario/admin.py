from django.contrib import admin
from .models import (
    CalendarioAcademico,
    Periodo,
    TipoFeriado,
    Feriado,
    TipoHorario,
    Horario,
    ClaseHorario
)

class PeriodoInline(admin.TabularInline):
    model = Periodo
    extra = 1

class FeriadoInline(admin.TabularInline):
    model = Feriado
    extra = 1

@admin.register(CalendarioAcademico)
class CalendarioAcademicoAdmin(admin.ModelAdmin):
    list_display = ('año', 'unidad_educativa', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('unidad_educativa', 'año', 'activo')
    search_fields = ('unidad_educativa__nombre',)
    inlines = [PeriodoInline, FeriadoInline]

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_division', 'calendario', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('calendario', 'tipo_division', 'estado')
    search_fields = ('nombre',)

@admin.register(TipoFeriado)
class TipoFeriadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'es_nacional')
    list_filter = ('es_nacional',)
    search_fields = ('nombre',)

@admin.register(Feriado)
class FeriadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'fecha', 'calendario')
    list_filter = ('tipo', 'calendario')
    search_fields = ('nombre',)
    date_hierarchy = 'fecha'

@admin.register(TipoHorario)
class TipoHorarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'turno')
    list_filter = ('turno',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'dia', 'hora_inicio', 'hora_fin')
    list_filter = ('tipo', 'dia')
    ordering = ('dia', 'hora_inicio')

@admin.register(ClaseHorario)
class ClaseHorarioAdmin(admin.ModelAdmin):
    list_display = ('clase', 'horario', 'fecha_inicio', 'fecha_fin')
    list_filter = ('clase', 'horario__dia')
    search_fields = ('clase__nombre',)
    date_hierarchy = 'fecha_inicio'