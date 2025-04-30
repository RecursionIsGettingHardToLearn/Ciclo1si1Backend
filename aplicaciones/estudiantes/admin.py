from django.contrib import admin
from .models import Estudiante, Tutor, TutorEstudiante

class TutorEstudianteInline(admin.TabularInline):
    model = TutorEstudiante
    extra = 1
    fk_name = 'estudiante'

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rude', 'curso', 'estado')
    list_filter = ('estado', 'curso')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'rude')
    inlines = [TutorEstudianteInline]

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'parentesco')
    list_filter = ('parentesco',)
    search_fields = ('usuario__nombre', 'usuario__apellido')

@admin.register(TutorEstudiante)
class TutorEstudianteAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'estudiante', 'es_principal', 'fecha_asignacion')
    list_filter = ('es_principal', 'fecha_asignacion')
    search_fields = (
        'tutor__usuario__nombre', 
        'tutor__usuario__apellido',
        'estudiante__usuario__nombre',
        'estudiante__usuario__apellido'
    )