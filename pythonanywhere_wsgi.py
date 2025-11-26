"""
WSGI config para PythonAnywhere

Este archivo debe ser copiado en la configuración WSGI de PythonAnywhere
en la pestaña Web -> WSGI configuration file

IMPORTANTE: Reemplaza 'TU_USUARIO' con tu nombre de usuario de PythonAnywhere
"""

import sys
import os

# ==============================================================================
# CONFIGURACIÓN - REEMPLAZA 'TU_USUARIO' CON TU USUARIO DE PYTHONANYWHERE
# ==============================================================================
USUARIO_PYTHONANYWHERE = 'TU_USUARIO'  # ¡¡¡CAMBIAR ESTO!!!
NOMBRE_PROYECTO = 'me_backend'
# ==============================================================================

# Agregar el directorio del proyecto al path
path = f'/home/{USUARIO_PYTHONANYWHERE}/{NOMBRE_PROYECTO}'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar el módulo de settings de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'portfolio_backend.settings'

# Variables de entorno (OPCIONAL - mejor usar .env)
# Descomenta y configura si no usas archivo .env:
# os.environ['SECRET_KEY'] = 'tu-secret-key-aqui'
# os.environ['DEBUG'] = 'False'
# os.environ['ALLOWED_HOSTS'] = f'{USUARIO_PYTHONANYWHERE}.pythonanywhere.com'

# Cargar variables de entorno desde archivo .env
# PythonAnywhere soporta python-decouple que ya tienes en requirements.txt
# Así que tu proyecto leerá el .env automáticamente

# Inicializar la aplicación Django WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

