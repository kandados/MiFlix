# Generated by Django 5.1.3 on 2024-12-06 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0007_calificacion"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuariocontenido",
            name="calificacion",
            field=models.FloatField(blank=True, null=True),
        ),
    ]