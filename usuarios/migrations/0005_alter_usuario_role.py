# Generated by Django 5.1.3 on 2024-11-19 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0004_usuariocontenido_visto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="role",
            field=models.CharField(
                choices=[
                    ("ADMIN", "Administrador"),
                    ("CLIENT", "Cliente"),
                    ("USER", "USUARIO"),
                ],
                default="CLIENT",
                max_length=10,
            ),
        ),
    ]
