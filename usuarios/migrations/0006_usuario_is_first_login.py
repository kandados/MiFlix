# Generated by Django 5.1.3 on 2024-11-23 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0005_alter_usuario_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="is_first_login",
            field=models.BooleanField(default=True),
        ),
    ]