# Generated by Django 5.1.2 on 2024-11-10 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenido", "0004_alter_contenido_genero"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contenido",
            name="image_card",
        ),
        migrations.AlterField(
            model_name="contenido",
            name="image_cover",
            field=models.ImageField(blank=True, null=True, upload_to="content_images/"),
        ),
        migrations.AlterField(
            model_name="contenido",
            name="video",
            field=models.FileField(blank=True, null=True, upload_to="content_videos/"),
        ),
    ]