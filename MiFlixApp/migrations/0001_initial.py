# Generated by Django 5.1.3 on 2024-11-17 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Pelicula",
            fields=[
                ("id", models.AutoField(default=1, primary_key=True, serialize=False)),
                ("titulo", models.CharField(max_length=255)),
                ("sinopsis", models.TextField(blank=True, null=True)),
                ("estreno", models.IntegerField(blank=True, null=True)),
                ("genero", models.CharField(blank=True, max_length=100, null=True)),
                ("director", models.CharField(blank=True, max_length=255, null=True)),
                ("protagonistas", models.TextField(blank=True, null=True)),
                ("duracion", models.IntegerField(blank=True, null=True)),
                ("calificacion_usuario", models.FloatField(blank=True, null=True)),
                ("vistas_totales", models.IntegerField(default=0)),
                (
                    "image_cover",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "Peliculas",
            },
        ),
        migrations.CreateModel(
            name="Serie",
            fields=[
                ("id", models.AutoField(default=1, primary_key=True, serialize=False)),
                ("titulo", models.CharField(max_length=255)),
                ("sinopsis", models.TextField(blank=True, null=True)),
                ("estreno", models.IntegerField(blank=True, null=True)),
                ("genero", models.CharField(blank=True, max_length=100, null=True)),
                ("director", models.CharField(blank=True, max_length=255, null=True)),
                ("protagonistas", models.TextField(blank=True, null=True)),
                ("temporadas_totales", models.IntegerField(blank=True, null=True)),
                ("capitulos_totales", models.IntegerField(blank=True, null=True)),
                ("duracion_media_capitulo", models.IntegerField(blank=True, null=True)),
                ("calificacion_usuario", models.FloatField(blank=True, null=True)),
                ("vistas_totales", models.IntegerField(default=0)),
                (
                    "image_cover",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "Series",
            },
        ),
    ]