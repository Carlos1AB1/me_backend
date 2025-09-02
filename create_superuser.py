#!/usr/bin/env python
"""
Script para crear un superusuario automáticamente si no existe
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

# Obtener credenciales del superusuario desde variables de entorno
admin_email = config('ADMIN_EMAIL', default='cabaton_23@cue.edu.co')
admin_username = config('ADMIN_USERNAME', default='admin')
admin_password = config('ADMIN_PASSWORD', default='Carlos111!')

# Crear superusuario si no existe
if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password
    )
    print(f"Superusuario '{admin_username}' creado exitosamente.")
else:
    print(f"Superusuario '{admin_username}' ya existe.")
