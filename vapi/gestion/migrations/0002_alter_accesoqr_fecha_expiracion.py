# Generated by Django 5.1.2 on 2024-10-20 23:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accesoqr",
            name="fecha_expiracion",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 10, 21, 0, 50, 53, 844801, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
