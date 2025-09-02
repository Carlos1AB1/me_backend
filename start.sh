#!/bin/bash

# Configurar variables
export DJANGO_SETTINGS_MODULE=portfolio_backend.settings

echo "=== Iniciando configuración del proyecto ==="

# Verificar conectividad de base de datos
echo "Verificando conexión a base de datos..."
python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection(); print('✅ Conexión a BD exitosa')" || {
    echo "❌ Error de conexión a BD. Continuando con SQLite..."
}

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --verbosity=2 || {
    echo "❌ Error en migraciones"
    exit 1
}

# Crear superusuario (no crítico si falla)
echo "Creando superusuario..."
python create_superuser.py || echo "⚠️ Superusuario no creado (puede que ya exista)"

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --verbosity=2 || {
    echo "❌ Error en collectstatic"
    exit 1
}

echo "=== Configuración completada. Iniciando servidor ==="

# Iniciar el servidor con gunicorn
exec gunicorn portfolio_backend.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 30 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
