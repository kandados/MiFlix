# Generated by Django 5.1.3 on 2024-12-07 11:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ClonFlixApp", "0004_alter_pelicula_options_alter_serie_options"),
        ("usuarios", "0008_usuariocontenido_calificacion"),
    ]

    operations = [
        migrations.CreateModel(
            name="UsuarioPelicula",
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
                ("visto", models.BooleanField(default=False)),
                ("fecha_visto", models.DateTimeField(auto_now_add=True)),
                (
                    "pelicula",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="usuarios_que_vieron",
                        to="ClonFlixApp.pelicula",
                    ),
                ),
                (
                    "usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="peliculas_vistas",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Película vista por usuario",
                "verbose_name_plural": "Películas vistas por usuarios",
                "unique_together": {("usuario", "pelicula")},
            },
        ),
    ]