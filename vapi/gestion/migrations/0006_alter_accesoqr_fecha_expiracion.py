# Generated by Django 5.1.2 on 2024-10-21 00:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0005_alter_accesoqr_fecha_expiracion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accesoqr",
            name="fecha_expiracion",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 10, 21, 1, 27, 56, 42262, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
