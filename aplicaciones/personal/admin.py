from django.contrib import admin
from .models import Profesor, Especialidad, ProfesorEspecialidad

class ProfesorEspecialidadInline(admin.TabularInline):
    model = ProfesorEspecialidad
    extra = 1

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'estado')
    list_filter = ('estado',)
    search_fields = ('usuario__nombre', 'usuario__apellido')
    inlines = [ProfesorEspecialidadInline]

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'materia')
    list_filter = ('materia',)
    search_fields = ('nombre', 'materia__nombre')

@admin.register(ProfesorEspecialidad)
class ProfesorEspecialidadAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'especialidad', 'fecha_asignacion')
    list_filter = ('especialidad', 'fecha_asignacion')
    search_fields = ('profesor__usuario__nombre', 'especialidad__nombre')