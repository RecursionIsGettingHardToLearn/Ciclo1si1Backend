from django.contrib import admin
from .models import Colegio, Modulo, Aula, UnidadEducativa

class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1

@admin.register(Colegio)
class ColegioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'direccion')
    list_filter = ('nombre',)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_aulas')
    search_fields = ('nombre',)
    inlines = [AulaInline]

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'modulo', 'tipo', 'capacidad', 'estado')
    list_filter = ('modulo', 'tipo', 'estado')
    search_fields = ('nombre', 'equipamiento')

@admin.register(UnidadEducativa)
class UnidadEducativaAdmin(admin.ModelAdmin):
    list_display = ('colegio', 'codigo_sie', 'turno')
    list_filter = ('colegio', 'turno')
    search_fields = ('codigo_sie', 'direccion')