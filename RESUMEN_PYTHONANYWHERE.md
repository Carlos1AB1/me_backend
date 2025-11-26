# 🚀 Resumen Rápido - Despliegue en PythonAnywhere

## ✅ Lo que ya está preparado:

1. ✅ **settings.py** actualizado con soporte para MySQL y PythonAnywhere
2. ✅ **requirements.txt** actualizado con mysqlclient
3. ✅ **pythonanywhere_wsgi.py** - archivo WSGI listo para copiar
4. ✅ **env.pythonanywhere.example** - plantilla de variables de entorno
5. ✅ **DESPLIEGUE_PYTHONANYWHERE.md** - guía completa paso a paso

---

## 📝 Pasos Rápidos (versión corta):

### 1️⃣ Crear cuenta
- Ve a [pythonanywhere.com](https://www.pythonanywhere.com) → Sign up (gratis)

### 2️⃣ Clonar repo
```bash
git clone https://github.com/TU_USUARIO/me_backend.git
cd me_backend
```

### 3️⃣ Crear virtualenv
```bash
mkvirtualenv --python=/usr/bin/python3.10 portfolio_env
pip install -r requirements.txt
```

### 4️⃣ Configurar base de datos
**Opción fácil (MySQL):**
- Databases tab → Initialize MySQL → Create password
- Create database: `portfolio_db`

**Opción más fácil (SQLite):**
- No hacer nada, usa SQLite por defecto

### 5️⃣ Crear archivo .env
```bash
nano .env
```
Copiar contenido de `env.pythonanywhere.example` y ajustar valores

### 6️⃣ Migraciones
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 7️⃣ Crear Web App
- Web tab → Add new web app
- Manual configuration → Python 3.10
- Source code: `/home/TU_USUARIO/me_backend`
- Virtualenv: `/home/TU_USUARIO/.virtualenvs/portfolio_env`

### 8️⃣ Configurar WSGI
- Web tab → WSGI configuration file
- Borrar todo y copiar contenido de `pythonanywhere_wsgi.py`
- Reemplazar `TU_USUARIO` con tu usuario real

### 9️⃣ Archivos estáticos
Static files section:
- URL: `/static/` → Directory: `/home/TU_USUARIO/me_backend/staticfiles/`

### 🔟 Reload
- Click en el botón verde "Reload"
- Visita: `https://tu-usuario.pythonanywhere.com`

---

## 🎯 URLs importantes:

- **API:** `https://tu-usuario.pythonanywhere.com/api/`
- **Swagger:** `https://tu-usuario.pythonanywhere.com/swagger/`
- **Admin:** `https://tu-usuario.pythonanywhere.com/admin/`

---

## 📚 Archivos importantes:

1. **DESPLIEGUE_PYTHONANYWHERE.md** - Guía completa con todos los detalles
2. **pythonanywhere_wsgi.py** - Copiar este contenido en el WSGI config
3. **env.pythonanywhere.example** - Plantilla para tu archivo .env

---

## 🆘 Si algo falla:

1. Revisar logs en Web tab → Log files → Error log
2. Verificar que reemplazaste `TU_USUARIO` en WSGI
3. Verificar que el .env tiene los valores correctos
4. Ejecutar: `workon portfolio_env` antes de cualquier comando Python

---

## 💰 Costo: **$0 - Gratis para siempre**

✅ No se suspende por inactividad  
✅ HTTPS incluido  
✅ 512MB espacio  
✅ No requiere tarjeta de crédito

---

**¡Lee DESPLIEGUE_PYTHONANYWHERE.md para la guía completa!**

