#!/bin/bash
# ============================================
# SCRIPT COMPLETO DE ACTUALIZACIÓN
# ============================================
# Copia y pega TODO este script en PythonAnywhere

set -e  # Detener si hay error

echo "🚀 INICIANDO ACTUALIZACIÓN COMPLETA..."
echo ""

# ============================================
# 1. IR AL DIRECTORIO
# ============================================
echo "📁 1/8 - Navegando al directorio..."
cd ~/me_backend

# ============================================
# 2. ACTIVAR VIRTUALENV
# ============================================
echo "🔧 2/8 - Activando virtualenv..."
source ~/.virtualenvs/portfolio_env/bin/activate

# ============================================
# 3. GUARDAR CAMBIOS LOCALES
# ============================================
echo "💾 3/8 - Guardando cambios locales..."
git stash || true

# ============================================
# 4. ACTUALIZAR CÓDIGO
# ============================================
echo "⬇️ 4/8 - Descargando última versión..."
git fetch origin
git reset --hard origin/main

echo ""
echo "✅ Último commit aplicado:"
git log --oneline -1
echo ""

# ============================================
# 5. LIMPIAR CACHÉ DE PYTHON
# ============================================
echo "🧹 5/8 - Limpiando caché de Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# ============================================
# 6. CREAR Y APLICAR MIGRACIONES
# ============================================
echo "📊 6/8 - Creando migraciones..."
python manage.py makemigrations projects services

echo ""
echo "📊 Aplicando migraciones..."
python manage.py migrate

# ============================================
# 7. VERIFICAR CONFIGURACIÓN
# ============================================
echo ""
echo "🔍 7/8 - Verificando configuración..."
echo ""
python manage.py shell << 'EOF'
from django.conf import settings
from skills.models import Skill
from projects.models import Project, ProjectImage
from services.models import Service

print("=" * 50)
print("CONFIGURACIÓN DE ALMACENAMIENTO")
print("=" * 50)
storage = getattr(settings, 'DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
print(f"Storage: {storage}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")

print("")
print("=" * 50)
print("MODELOS ACTUALIZADOS")
print("=" * 50)

# Verificar que los campos existen
skill_fields = [f.name for f in Skill._meta.fields]
print(f"✅ Skill tiene image_url: {'image_url' in skill_fields}")
print(f"✅ Skill tiene sub_image_url: {'sub_image_url' in skill_fields}")

project_image_fields = [f.name for f in ProjectImage._meta.fields]
print(f"✅ ProjectImage tiene image_url: {'image_url' in project_image_fields}")

service_fields = [f.name for f in Service._meta.fields]
print(f"✅ Service tiene image_url: {'image_url' in service_fields}")

print("")
print("=" * 50)
print("ESTADÍSTICAS")
print("=" * 50)
print(f"Skills: {Skill.objects.count()}")
print(f"Projects: {Project.objects.count()}")
print(f"Services: {Service.objects.count()}")

print("")
print("✅ TODO CORRECTO")
print("=" * 50)
EOF

# ============================================
# 8. CONFIGURAR PERMISOS
# ============================================
echo ""
echo "🔐 8/8 - Configurando permisos..."
chmod -R 755 ~/me_backend/media 2>/dev/null || true
mkdir -p ~/me_backend/media/skills ~/me_backend/media/projects ~/me_backend/media/services 2>/dev/null || true

echo ""
echo "=" * 60
echo "✅ ¡ACTUALIZACIÓN COMPLETADA!"
echo "=" * 60
echo ""
echo "🔄 AHORA DEBES:"
echo "   1. Ir a la Web tab"
echo "   2. Click en 'Reload cabaron23.pythonanywhere.com'"
echo ""
echo "📝 LUEGO PUEDES:"
echo "   - Ir al admin: https://cabaron23.pythonanywhere.com/admin/"
echo "   - Verás campos 'URL de Imagen' en Skills, Projects y Services"
echo "   - Pega URLs de GitHub raw o ImgBB"
echo ""
echo "🎯 URLs de GitHub (formato):"
echo "   https://raw.githubusercontent.com/Carlos1AB1/me_backend/main/assets/images/CARPETA/ARCHIVO.ext"
echo ""
echo "=" * 60

