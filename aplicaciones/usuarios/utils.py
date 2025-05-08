# usuarios/utils.py
from usuarios.models import Bitacora
from django.utils import timezone

def registrar_bitacora(usuario, ip, tabla, accion, descripcion=""):
    Bitacora.objects.create(
        usuario=usuario,
        ip=ip,
        hora_entrada=timezone.now(),
        tabla=tabla,
        accion=accion,
        descripcion=descripcion
    )
