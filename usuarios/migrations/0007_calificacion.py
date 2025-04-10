# Generated by Django 5.1.3 on 2024-12-06 10:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MiFlixApp", "0004_alter_pelicula_options_alter_serie_options"),
        ("usuarios", "0006_usuario_is_first_login"),
    ]

    operations = [
        migrations.CreateModel(
            name="Calificacion",
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
                ("calificacion", models.PositiveSmallIntegerField()),
                (
                    "pelicula",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MiFlixApp.pelicula",
                    ),
                ),
                (
                    "serie",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MiFlixApp.serie",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Calificación",
                "verbose_name_plural": "Calificaciones",
                "unique_together": {("usuario", "pelicula", "serie")},
            },
        ),
    ]
