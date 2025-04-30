from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    DimensionEvaluacion,
    Actividad,
    NotaActividad,
    NotaFinalMateria,
    AutoEvaluacion
)

class NotaActividadInline(admin.TabularInline):
    model = NotaActividad
    extra = 1

@admin.register(DimensionEvaluacion)
class DimensionEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'ponderacion', 'periodo')
    list_filter = ('tipo', 'periodo')
    search_fields = ('nombre',)

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'materia_curso', 'dimension', 'fecha', 'nota_maxima')
    list_filter = ('materia_curso', 'dimension', 'es_recuperacion')
    search_fields = ('nombre', 'descripcion')
    inlines = [NotaActividadInline]

@admin.register(NotaActividad)
class NotaActividadAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'actividad', 'nota_obtenida', 'fecha_registro')
    list_filter = ('actividad__materia_curso', 'actividad__dimension')
    search_fields = ('estudiante__usuario__nombre', 'actividad__nombre')

@admin.register(NotaFinalMateria)
class NotaFinalMateriaAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'materia_curso', 'periodo', 'nota_final', 'estado')
    list_filter = ('materia_curso', 'periodo', 'estado')
    search_fields = ('estudiante__usuario__nombre', 'materia_curso__curso__nombre')

@admin.register(AutoEvaluacion)
class AutoEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'materia_curso', 'dimension', 'nota', 'fecha')
    list_filter = ('materia_curso', 'periodo', 'dimension')
    search_fields = ('estudiante__usuario__nombre', 'comentario')