#!/bin/bash
# Script para actualizar el código en PythonAnywhere
# Ejecutar en la consola Bash de PythonAnywhere

echo "🔄 Actualizando código en PythonAnywhere..."

# Ir al directorio
cd ~/me_backend

# Activar virtualenv
source ~/.virtualenvs/portfolio_env/bin/activate

# Guardar cambios locales si hay
echo "📦 Guardando cambios locales..."
git stash

# Obtener la última versión
echo "⬇️ Obteniendo última versión..."
git fetch origin

# Forzar actualización
echo "🔨 Forzando actualización..."
git reset --hard origin/main

# Verificar que se actualizó
echo "✅ Verificando actualización..."
echo ""
echo "Último commit:"
git log --oneline -1
echo ""

# Verificar configuración de Cloudinary
echo "🔍 Verificando configuración de almacenamiento..."
echo "DEFAULT_FILE_STORAGE debe estar comentado (#):"
grep -n "DEFAULT_FILE_STORAGE" portfolio_backend/settings.py
echo ""
echo "MEDIA_ROOT debe existir:"
grep -n "MEDIA_ROOT" portfolio_backend/settings.py
echo ""

# Aplicar migraciones
echo "📊 Aplicando migraciones..."
python manage.py migrate

# Verificar en Django shell
echo "🐍 Verificando configuración en Django..."
python manage.py shell << EOF
from django.conf import settings
print("\n=== CONFIGURACIÓN ACTUAL ===")
print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print("============================\n")
EOF

echo ""
echo "✅ ¡Actualización completada!"
echo ""
echo "🔄 IMPORTANTE: Ahora ve a la Web tab y haz RELOAD"
echo ""

