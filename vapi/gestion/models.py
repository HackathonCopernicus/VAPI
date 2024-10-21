from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import timedelta
from django.utils import timezone
from visor.models import Finca

class UsuarioTecnico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Vinculación con el modelo por defecto de usuarios de Django
    descripcion = models.TextField(blank=True)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True)
    campo_especialidad = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
    
class UsuarioCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Vinculación con el modelo de usuarios
    finca_asociada = models.ForeignKey(Finca, on_delete=models.SET_NULL, null=True, blank=True)  # Un cliente puede tener una finca asociada (no obligatorio)
    
    def __str__(self):
        return self.user.username

class AccesoQR(models.Model):
    tecnico = models.ForeignKey(UsuarioTecnico, on_delete=models.CASCADE)
    codigo_qr = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Genera un UUID único para el QR
    activo = models.BooleanField(default=True)  # Indica si el acceso está activo
    fecha_expiracion = models.DateTimeField(default=timezone.now() + timedelta(hours=1))  # Tiempo de expiración

    def expirar(self):
        """Función para desactivar el acceso cuando expira."""
        if timezone.now() > self.fecha_expiracion:
            self.activo = False
            self.save()

    def __str__(self):
        return str(self.codigo_qr)

