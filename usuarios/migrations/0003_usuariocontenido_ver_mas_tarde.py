# Generated by Django 5.1.2 on 2024-11-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0002_usuariocontenido_delete_contenido"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuariocontenido",
            name="ver_mas_tarde",
            field=models.BooleanField(default=False),
        ),
    ]