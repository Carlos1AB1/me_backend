#!/bin/bash
# Script para ejecutar el frontend Next.js localmente

echo "🚀 CONFIGURANDO FRONTEND..."
echo ""

cd /Users/prueba/Desktop/me_backend/me

# Verificar si node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias de Node.js..."
    npm install
    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya instaladas"
fi

echo ""
echo "========================================="
echo "✅ FRONTEND LISTO"
echo "========================================="
echo ""
echo "🎯 PARA EJECUTAR:"
echo "   cd /Users/prueba/Desktop/me_backend/me"
echo "   npm run dev"
echo ""
echo "🌐 LUEGO ACCEDE A:"
echo "   http://localhost:3000"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - El backend debe estar corriendo en: http://127.0.0.1:8000"
echo "   - O cambia la URL en me/lib/api.ts"
echo ""

