#!/bin/bash
# Script para ejecutar el proyecto localmente en Mac

echo "🚀 CONFIGURANDO ENTORNO LOCAL..."
echo ""

cd /Users/prueba/Desktop/me_backend

# Verificar si existe virtualenv
if [ ! -d "venv" ]; then
    echo "📦 Creando virtualenv..."
    python3 -m venv venv
    echo "✅ Virtualenv creado"
else
    echo "✅ Virtualenv ya existe"
fi

# Activar virtualenv
echo "🔧 Activando virtualenv..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo ""
echo "✅ DEPENDENCIAS INSTALADAS"
echo ""

# Ver datos
echo "📊 MOSTRANDO DATOS DE LA BASE DE DATOS LOCAL..."
echo ""
python ver_datos_bd.py

echo ""
echo "========================================="
echo "✅ SCRIPT COMPLETADO"
echo "========================================="
echo ""
echo "🎯 PARA EJECUTAR EL SERVIDOR:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "🌐 LUEGO ACCEDE A:"
echo "   http://127.0.0.1:8000/admin/"
echo ""

