# Generated by Django 5.1.2 on 2024-11-10 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenido", "0002_contenido_image_card"),
    ]

    operations = [
        migrations.AddField(
            model_name="contenido",
            name="actores",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contenido",
            name="calificacion_usuario",
            field=models.DecimalField(
                blank=True, decimal_places=1, max_digits=3, null=True
            ),
        ),
        migrations.AddField(
            model_name="contenido",
            name="capitulos_totales",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contenido",
            name="director",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contenido",
            name="duracion",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contenido",
            name="genero",
            field=models.CharField(
                blank=True,
                choices=[
                    ("action", "Acción"),
                    ("comedy", "Comedia"),
                    ("drama", "Drama"),
                    ("horror", "Terror"),
                    ("romance", "Romance"),
                    ("science_fiction", "Ciencia Ficción"),
                    ("fantasy", "Fantasía"),
                ],
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="contenido",
            name="image_cover",
            field=models.ImageField(blank=True, null=True, upload_to="movie_images/"),
        ),
        migrations.AddField(
            model_name="contenido",
            name="temporadas_totales",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contenido",
            name="video",
            field=models.FileField(blank=True, null=True, upload_to="movie_videos/"),
        ),
        migrations.AddField(
            model_name="contenido",
            name="vistas_totales",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="contenido",
            name="image_card",
            field=models.ImageField(blank=True, null=True, upload_to="movie_images/"),
        ),
        migrations.AlterField(
            model_name="contenido",
            name="titulo",
            field=models.CharField(max_length=255),
        ),
    ]