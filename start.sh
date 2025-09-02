#!/bin/bash

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario automáticamente
python create_superuser.py

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Iniciar el servidor con gunicorn
gunicorn portfolio_backend.wsgi:application --bind 0.0.0.0:$PORT
