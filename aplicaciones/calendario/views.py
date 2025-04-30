from rest_framework import viewsets
from .models import (
    CalendarioAcademico,
    Periodo,
    TipoFeriado,
    Feriado,
    TipoHorario,
    Horario,
    ClaseHorario
)
from .serializers import (
    CalendarioAcademicoSerializer,
    PeriodoSerializer,
    TipoFeriadoSerializer,
    FeriadoSerializer,
    TipoHorarioSerializer,
    HorarioSerializer,
    ClaseHorarioSerializer,
    CreateCalendarioAcademicoSerializer,
    CreatePeriodoSerializer,
    CreateFeriadoSerializer,
    CreateHorarioSerializer,
    CreateClaseHorarioSerializer
)

class CalendarioAcademicoViewSet(viewsets.ModelViewSet):
    queryset = CalendarioAcademico.objects.all()
    filterset_fields = ['unidad_educativa', 'año', 'activo']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateCalendarioAcademicoSerializer
        return CalendarioAcademicoSerializer

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    filterset_fields = ['calendario', 'tipo_division', 'estado']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreatePeriodoSerializer
        return PeriodoSerializer

class TipoFeriadoViewSet(viewsets.ModelViewSet):
    queryset = TipoFeriado.objects.all()
    serializer_class = TipoFeriadoSerializer
    filterset_fields = ['es_nacional']
    search_fields = ['nombre']

class FeriadoViewSet(viewsets.ModelViewSet):
    queryset = Feriado.objects.all()
    filterset_fields = ['calendario', 'tipo', 'fecha']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateFeriadoSerializer
        return FeriadoSerializer

class TipoHorarioViewSet(viewsets.ModelViewSet):
    queryset = TipoHorario.objects.all()
    serializer_class = TipoHorarioSerializer
    search_fields = ['nombre', 'descripcion']

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    filterset_fields = ['tipo', 'dia']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateHorarioSerializer
        return HorarioSerializer

class ClaseHorarioViewSet(viewsets.ModelViewSet):
    queryset = ClaseHorario.objects.all()
    filterset_fields = ['clase', 'horario']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateClaseHorarioSerializer
        return ClaseHorarioSerializer