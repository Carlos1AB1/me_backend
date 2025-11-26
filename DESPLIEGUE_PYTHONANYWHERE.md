# 🚀 Guía de Despliegue en PythonAnywhere

Esta guía te ayudará a desplegar tu backend de Django en PythonAnywhere de forma **100% gratuita**.

## 📋 Requisitos Previos

- [ ] Cuenta de GitHub con tu repositorio
- [ ] Cuenta de Cloudinary (para imágenes)
- [ ] 30 minutos de tiempo

---

## 🎯 Paso 1: Crear Cuenta en PythonAnywhere

1. Ve a [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Haz clic en **"Start running Python online for FREE"**
3. Crea tu cuenta (elige un nombre de usuario corto y memorable)
4. **NO requiere tarjeta de crédito** ✅

---

## 🔧 Paso 2: Clonar tu Repositorio

### 2.1. Abrir una Consola Bash
1. En el dashboard de PythonAnywhere, ve a la pestaña **"Consoles"**
2. Haz clic en **"Bash"** para abrir una nueva consola

### 2.2. Clonar tu proyecto
```bash
# Clonar tu repositorio
git clone https://github.com/TU_USUARIO/me_backend.git
cd me_backend
```

---

## 🐍 Paso 3: Configurar Entorno Virtual

### 3.1. Crear virtualenv con Python 3.10
```bash
mkvirtualenv --python=/usr/bin/python3.10 portfolio_env
```

### 3.2. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

⏱️ **Esto puede tomar 3-5 minutos**

---

## 🗄️ Paso 4: Configurar Base de Datos

Tienes **3 opciones**. Elige la que prefieras:

### Opción A: MySQL (Recomendado para PythonAnywhere) ⭐

#### 4.1. Crear base de datos MySQL
1. Ve a la pestaña **"Databases"** en PythonAnywhere
2. Haz clic en **"Initialize MySQL"**
3. Crea una contraseña para MySQL
4. En "Create database", ingresa: `portfolio_db`
5. Anota estos datos:
   - Host: `TU_USUARIO.mysql.pythonanywhere-services.com`
   - Usuario: `TU_USUARIO`
   - Base de datos: `TU_USUARIO$portfolio_db`

#### 4.2. Crear archivo .env
```bash
cd ~/me_backend
nano .env
```

Pega este contenido (reemplaza los valores):
```bash
# Configuración General
SECRET_KEY=tu-secret-key-super-segura-aqui-genera-una-nueva
DEBUG=False
ALLOWED_HOSTS=tu-usuario.pythonanywhere.com

# Base de datos MySQL
DB_ENGINE=mysql
DB_NAME=tu_usuario$portfolio_db
DB_USER=tu_usuario
DB_PASSWORD=tu-password-mysql
DB_HOST=tu_usuario.mysql.pythonanywhere-services.com

# Cloudinary (copia tus credenciales actuales)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret

# CORS (agrega la URL de tu frontend)
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app,https://arturo.engineer
```

Guardar: `Ctrl+O`, Enter, `Ctrl+X`

### Opción B: SQLite (Más simple, para proyectos pequeños)

```bash
cd ~/me_backend
nano .env
```

```bash
SECRET_KEY=tu-secret-key-super-segura
DEBUG=False
ALLOWED_HOSTS=tu-usuario.pythonanywhere.com
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
```

### Opción C: PostgreSQL Externo (Neon.tech)

Si prefieres PostgreSQL, usa un servicio gratuito externo:
1. Crea cuenta en [Neon.tech](https://neon.tech) (gratis)
2. Crea una base de datos
3. Copia la DATABASE_URL
4. En tu .env:

```bash
DATABASE_URL=postgresql://usuario:password@host/database
SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=tu-usuario.pythonanywhere.com
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
CORS_ALLOWED_ORIGINS=https://tu-frontend.vercel.app
```

---

## 🔨 Paso 5: Ejecutar Migraciones y Recolectar Estáticos

```bash
cd ~/me_backend

# Asegúrate de que el virtualenv esté activado
workon portfolio_env

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario (opcional pero recomendado)
python manage.py createsuperuser
```

---

## 🌐 Paso 6: Configurar Web App

### 6.1. Crear nueva Web App
1. Ve a la pestaña **"Web"**
2. Haz clic en **"Add a new web app"**
3. Haz clic en **"Next"** (acepta el dominio gratuito)
4. Selecciona **"Manual configuration"**
5. Selecciona **"Python 3.10"**
6. Haz clic en **"Next"**

### 6.2. Configurar Code
En la sección **"Code"**:
- **Source code:** `/home/TU_USUARIO/me_backend`
- **Working directory:** `/home/TU_USUARIO/me_backend`

### 6.3. Configurar Virtualenv
En la sección **"Virtualenv"**:
- Ingresa: `/home/TU_USUARIO/.virtualenvs/portfolio_env`
- Haz clic en el check ✓

---

## 📝 Paso 7: Configurar WSGI

### 7.1. Editar archivo WSGI
1. En la pestaña "Web", busca la sección **"Code"**
2. Haz clic en el enlace **"WSGI configuration file"** (ej: `/var/www/tu_usuario_pythonanywhere_com_wsgi.py`)
3. **BORRA TODO EL CONTENIDO** del archivo
4. Copia y pega este código (reemplaza `TU_USUARIO`):

```python
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

# Cargar variables de entorno desde archivo .env
# PythonAnywhere soporta python-decouple que ya tienes instalado

# Inicializar la aplicación Django WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. Haz clic en **"Save"**

---

## 📁 Paso 8: Configurar Archivos Estáticos

En la pestaña **"Web"**, baja a la sección **"Static files"**:

### Agregar entrada para archivos estáticos:
- **URL:** `/static/`
- **Directory:** `/home/TU_USUARIO/me_backend/staticfiles/`

### (Opcional) Agregar entrada para media files locales:
- **URL:** `/media/`
- **Directory:** `/home/TU_USUARIO/me_backend/media/`

> **Nota:** Como usas Cloudinary, los media files se sirven desde allá, pero es bueno tener esto configurado por si acaso.

---

## 🚀 Paso 9: Reload y Probar

### 9.1. Reload de la aplicación
1. En la parte superior de la pestaña **"Web"**
2. Haz clic en el botón verde grande: **"Reload tu_usuario.pythonanywhere.com"**

### 9.2. Verificar que funciona
1. Haz clic en el enlace de tu sitio: `https://tu-usuario.pythonanywhere.com`
2. Deberías ver tu API

### 9.3. Probar endpoints
```bash
# API root
https://tu-usuario.pythonanywhere.com/api/

# Swagger docs
https://tu-usuario.pythonanywhere.com/swagger/

# Projects
https://tu-usuario.pythonanywhere.com/api/projects/

# Skills
https://tu-usuario.pythonanywhere.com/api/skills/

# Services
https://tu-usuario.pythonanywhere.com/api/services/

# Blog
https://tu-usuario.pythonanywhere.com/api/blog/

# Admin
https://tu-usuario.pythonanywhere.com/admin/
```

---

## 🔍 Paso 10: Verificar Logs (Si hay errores)

Si algo no funciona:

1. En la pestaña **"Web"**, baja a **"Log files"**
2. Revisa:
   - **Error log:** Muestra errores de Python/Django
   - **Server log:** Muestra logs del servidor
   - **Access log:** Muestra peticiones HTTP

### Errores comunes:

#### Error: "ImportError: No module named..."
```bash
# Solución: Reinstalar dependencias
workon portfolio_env
cd ~/me_backend
pip install -r requirements.txt
```

#### Error: "DisallowedHost"
```bash
# Solución: Verificar .env
cat ~/me_backend/.env | grep ALLOWED_HOSTS

# Debe tener:
ALLOWED_HOSTS=tu-usuario.pythonanywhere.com
```

#### Error: "OperationalError: unable to open database"
```bash
# Para SQLite, dar permisos:
chmod 644 ~/me_backend/db.sqlite3
chmod 755 ~/me_backend
```

#### Error: "Static files not found"
```bash
# Recolectar estáticos nuevamente
cd ~/me_backend
workon portfolio_env
python manage.py collectstatic --noinput --clear
```

---

## 🔄 Paso 11: Actualizar tu Aplicación (Deploy futuro)

Cuando hagas cambios a tu código:

```bash
# 1. Conectar a consola Bash en PythonAnywhere
cd ~/me_backend

# 2. Activar virtualenv
workon portfolio_env

# 3. Actualizar código
git pull origin main

# 4. Instalar nuevas dependencias (si hay)
pip install -r requirements.txt

# 5. Ejecutar migraciones (si hay cambios en modelos)
python manage.py migrate

# 6. Recolectar estáticos (si hay cambios en CSS/JS)
python manage.py collectstatic --noinput

# 7. Reload de la web app
# Ve a la pestaña Web y haz clic en "Reload"
```

O usa este script rápido:
```bash
cd ~/me_backend && workon portfolio_env && git pull && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && echo "¡Listo! Ahora ve a la pestaña Web y haz clic en Reload"
```

---

## 🎨 Paso 12: Actualizar tu Frontend

En tu frontend (Vercel), actualiza la URL del API:

```javascript
// Antes:
const API_URL = 'https://me-backend-vguc.onrender.com/api';

// Después:
const API_URL = 'https://tu-usuario.pythonanywhere.com/api';
```

---

## ✅ Checklist Final

Antes de dar por terminado el despliegue, verifica:

- [ ] El sitio carga sin errores: `https://tu-usuario.pythonanywhere.com`
- [ ] Swagger funciona: `https://tu-usuario.pythonanywhere.com/swagger/`
- [ ] Admin funciona: `https://tu-usuario.pythonanywhere.com/admin/`
- [ ] Los endpoints de API responden correctamente
- [ ] Las imágenes de Cloudinary se cargan
- [ ] El frontend puede conectarse al backend (CORS configurado)
- [ ] Puedes hacer login en el admin
- [ ] Los archivos estáticos (CSS del admin) se cargan correctamente

---

## 🎉 ¡Felicidades!

Tu backend está desplegado en PythonAnywhere **gratis y para siempre**. 

### 📊 Recursos del Plan Gratuito:
- ✅ **Sitio siempre activo** (no se suspende)
- ✅ **512 MB de almacenamiento**
- ✅ **HTTPS incluido**
- ✅ **100 segundos de CPU al día**
- ✅ **Subdomain:** `tu-usuario.pythonanywhere.com`

### 🚀 Si necesitas más recursos:
- **$5/meses:** Sin límites de CPU, dominio personalizado, más storage
- Pero el plan gratuito es suficiente para proyectos portfolio

---

## 🆘 Soporte

### Si algo no funciona:

1. **Revisa los logs** en la pestaña Web
2. **Consulta la documentación:** [help.pythonanywhere.com](https://help.pythonanywhere.com)
3. **Forum de PythonAnywhere:** Muy activo y útil
4. **Verificar configuración:** Asegúrate de haber reemplazado `TU_USUARIO` en todos los archivos

---

## 📚 Recursos Útiles

- [Documentación oficial PythonAnywhere + Django](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Configuración de MySQL en PythonAnywhere](https://help.pythonanywhere.com/pages/MySQLdb/)
- [Debugging en PythonAnywhere](https://help.pythonanywhere.com/pages/DebuggingImportError/)

---

**¡Tu portfolio backend ahora está en producción!** 🎊

