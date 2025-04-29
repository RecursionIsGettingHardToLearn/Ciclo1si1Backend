set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Crear superusuario personalizado si no existe
if [ "$CREATE_SUPERUSER" = "true" ]; then
  python manage.py shell << END
from django.contrib.auth import get_user_model
from usuarios.models import Rol

User = get_user_model()

# Crear rol de SuperAdmin si no existe
rol_superadmin, created = Rol.objects.get_or_create(
    nombre='SuperAdmin',
    defaults={'descripcion': 'Rol de superadministrador del sistema'}
)

if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    usuario_superadmin = User.objects.create_superuser(
        ci="987654321",  # Cédula de identidad
        email="${DJANGO_SUPERUSER_EMAIL}",  # Email
        nombre="Carlos",  # Nombre
        apellido="Gómez",  # Apellido
        username="${DJANGO_SUPERUSER_USERNAME}",
        password="${DJANGO_SUPERUSER_PASSWORD}",  # Contraseña
        rol=rol_superadmin
    )
    print(f"Superusuario creado: {usuario_superadmin.get_full_name()}")
else:
    print("El superusuario ya existe")
END
fi