from django.db import models
from django.contrib.gis.db import models as gis_models

from django.contrib.auth.models import User

class Finca(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    path = models.CharField(max_length=255, blank=True)  # Dirección para teselas o datos extra
    bounds = gis_models.PolygonField()  # Usamos un campo PostGIS para definir límites
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con técnico que gestiona la finca
    
    def __str__(self):
        return self.nombre

class Nota(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE, related_name="notas")
    referencia_geojson = gis_models.GeometryField()  # Campo para almacenar figuras geométricas

    def __str__(self):
        return self.titulo


