# Generated by Django 5.1.2 on 2024-10-20 23:25

import datetime
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("visor", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UsuarioCliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "finca_asociada",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="visor.finca",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UsuarioTecnico",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("descripcion", models.TextField(blank=True)),
                (
                    "foto_perfil",
                    models.ImageField(blank=True, upload_to="fotos_perfil/"),
                ),
                ("campo_especialidad", models.CharField(max_length=255)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AccesoQR",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "codigo_qr",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("activo", models.BooleanField(default=True)),
                (
                    "fecha_expiracion",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2024,
                            10,
                            21,
                            0,
                            25,
                            28,
                            850954,
                            tzinfo=datetime.timezone.utc,
                        )
                    ),
                ),
                (
                    "tecnico",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="gestion.usuariotecnico",
                    ),
                ),
            ],
        ),
    ]
