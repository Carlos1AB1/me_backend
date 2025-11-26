#!/bin/bash
# ============================================
# Comandos útiles para PythonAnywhere
# ============================================
# NO ejecutar este archivo directamente
# Copia y pega los comandos que necesites
# ============================================

# ========== SETUP INICIAL ==========

# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/me_backend.git
cd me_backend

# 2. Crear virtualenv
mkvirtualenv --python=/usr/bin/python3.10 portfolio_env

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 6. Crear superusuario
python manage.py createsuperuser

# ========== ACTUALIZAR APLICACIÓN ==========

# Script completo para actualizar (copia todo esto):
cd ~/me_backend && \
workon portfolio_env && \
git pull origin main && \
pip install -r requirements.txt && \
python manage.py migrate && \
python manage.py collectstatic --noinput && \
echo "✅ Actualización completa. Ahora ve a la pestaña Web y haz clic en Reload"

# ========== COMANDOS DE DJANGO ÚTILES ==========

# Activar virtualenv
workon portfolio_env

# Entrar a shell de Django
cd ~/me_backend
python manage.py shell

# Ver migraciones
python manage.py showmigrations

# Crear nuevas migraciones (si cambiaste modelos)
python manage.py makemigrations

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario adicional
python manage.py createsuperuser

# Limpiar y recolectar estáticos
python manage.py collectstatic --noinput --clear

# Verificar configuración
python manage.py check

# Ver información de la base de datos
python manage.py dbshell

# ========== COMANDOS DE GIT ==========

# Actualizar código desde GitHub
cd ~/me_backend
git pull origin main

# Ver estado
git status

# Ver cambios
git log --oneline -5

# Cambiar de rama
git checkout nombre-rama

# ========== GESTIÓN DE BASE DE DATOS ==========

# Para MySQL - Conectar a la base de datos
mysql -h TU_USUARIO.mysql.pythonanywhere-services.com -u TU_USUARIO -p

# Para SQLite - Conectar a la base de datos
cd ~/me_backend
sqlite3 db.sqlite3

# Backup de base de datos SQLite
cd ~/me_backend
cp db.sqlite3 db.sqlite3.backup_$(date +%Y%m%d_%H%M%S)

# ========== LOGS Y DEBUG ==========

# Ver últimas líneas del error log
tail -n 50 /var/log/TU_USUARIO.pythonanywhere.com.error.log

# Ver últimas líneas del server log
tail -n 50 /var/log/TU_USUARIO.pythonanywhere.com.server.log

# Seguir el error log en tiempo real
tail -f /var/log/TU_USUARIO.pythonanywhere.com.error.log

# ========== GESTIÓN DE ARCHIVOS ==========

# Ver tamaño de directorios
du -sh ~/me_backend/*

# Limpiar archivos de caché de Python
find ~/me_backend -type d -name "__pycache__" -exec rm -r {} +
find ~/me_backend -type f -name "*.pyc" -delete

# Ver espacio usado
quota

# ========== VIRTUALENV ==========

# Listar virtualenvs
lsvirtualenv

# Activar virtualenv
workon portfolio_env

# Desactivar virtualenv
deactivate

# Eliminar virtualenv (cuidado!)
rmvirtualenv nombre_env

# Ver paquetes instalados
pip list

# Ver paquetes desactualizados
pip list --outdated

# ========== VARIABLES DE ENTORNO ==========

# Editar archivo .env
nano ~/me_backend/.env

# Ver variables de entorno
cat ~/me_backend/.env

# Generar nueva SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# ========== TAREAS PERIÓDICAS (Para planes pagos) ==========

# Los planes gratuitos no tienen scheduled tasks
# Pero si actualizas, puedes programar tareas como:
# - Backups automáticos
# - Limpieza de datos antiguos
# - Envío de emails periódicos

# ========== COMANDOS DE POBLACIÓN DE DATOS ==========

# Si tienes comandos de management personalizados:
python manage.py populate_blog
python manage.py populate_services
python manage.py load_sample_data

# ========== INFORMACIÓN DEL SISTEMA ==========

# Ver versión de Python
python --version

# Ver ubicación de Python
which python

# Ver PATH
echo $PATH

# Ver info del virtualenv activo
echo $VIRTUAL_ENV

# ========== PERMISOS (Si hay problemas) ==========

# Dar permisos a db.sqlite3
chmod 644 ~/me_backend/db.sqlite3
chmod 755 ~/me_backend

# Dar permisos a directorio media
chmod -R 755 ~/me_backend/media

# Dar permisos a directorio staticfiles
chmod -R 755 ~/me_backend/staticfiles

# ============================================
# NOTAS:
# ============================================
# - Siempre activa el virtualenv antes de ejecutar comandos Python
# - Después de cambios en código, haz Reload en la pestaña Web
# - Los logs están en la pestaña Web → Log files
# - Reemplaza TU_USUARIO con tu nombre de usuario real
# ============================================

