from django.contrib import admin
from .models import UsuarioTecnico, UsuarioCliente, AccesoQR

admin.site.register(UsuarioTecnico)
admin.site.register(UsuarioCliente)
admin.site.register(AccesoQR)