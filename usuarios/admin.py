from django.contrib import admin

# Register your models here.
# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario  # Asegúrate de importar tu modelo de usuario personalizado

# Registrar el usuario personalizado en el panel de administración
admin.site.register(Usuario, UserAdmin)