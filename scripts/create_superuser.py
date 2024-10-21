import os
import django
import getpass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vapi.settings")
django.setup()

from django.contrib.auth.models import User

# Obtener el correo electrónico proporcionado
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

# Obtener la contraseña del superusuario desde la variable de entorno o solicitarla si no está definida
password = getpass.getpass("Por favor escribe tu contraseña para el superusuario: ")

# Definir el nombre de usuario del superusuario
username = "admin"

# Verificar si ya existe un superusuario con el nombre de usuario dado
if not User.objects.filter(username=username).exists():
    # Crear un superusuario con el correo electrónico y la contraseña proporcionados
    User.objects.create_superuser(username, email, password)
    print('Super usuario creado de forma exitosa')
else:
    print('El super usuario ya existe')
