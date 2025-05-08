# usuarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, SuperAdmin

@receiver(post_save, sender=Usuario)
def crear_superadmin_si_corresponde(sender, instance, created, **kwargs):
    if created and instance.rol.nombre == 'superadmin':
        SuperAdmin.objects.get_or_create(usuario=instance)
