# 🖥️ Ejecutar Proyecto Localmente

## 🚀 PASOS RÁPIDOS

### 1️⃣ Crear entorno virtual (si no existe)

```bash
cd /Users/prueba/Desktop/me_backend
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3️⃣ Ver datos de la BD local

```bash
python ver_datos_bd.py
```

### 4️⃣ Ejecutar servidor local

```bash
python manage.py runserver
```

Accede a: http://127.0.0.1:8000

---

## 📊 VER DATOS SIN EJECUTAR SERVIDOR

Si solo quieres ver qué datos tienes:

```bash
cd /Users/prueba/Desktop/me_backend
source venv/bin/activate  # Si usas virtualenv
python ver_datos_bd.py
```

Esto te mostrará:
- ✅ Todos los Skills
- ✅ Todos los Projects
- ✅ Todos los Services
- ✅ Estado de imágenes
- ✅ Categorías
- ✅ Usuarios

---

## 🗄️ BASES DE DATOS

### **Local (SQLite):**
```
Archivo: db.sqlite3
Ubicación: /Users/prueba/Desktop/me_backend/db.sqlite3
```

### **PythonAnywhere (MySQL):**
```
Host: cabaron23.mysql.pythonanywhere-services.com
Base de datos: cabaron23$default
Usuario: cabaron23
```

**SON BASES DE DATOS DIFERENTES**
- Los datos en local NO están en PythonAnywhere
- Los datos en PythonAnywhere NO están en local
- Si quieres sincronizar, hay que exportar/importar

---

## 🔄 SINCRONIZAR DATOS (Opcional)

### Opción A: Exportar desde local a PythonAnywhere

```bash
# 1. Exportar datos locales
python manage.py dumpdata skills projects services blog > datos.json

# 2. Subir a Git
git add datos.json
git commit -m "Export data"
git push

# 3. En PythonAnywhere
cd ~/me_backend
workon portfolio_env
git pull
python manage.py loaddata datos.json
```

### Opción B: Exportar desde PythonAnywhere a local

```bash
# 1. En PythonAnywhere
cd ~/me_backend
workon portfolio_env
python manage.py dumpdata skills projects services blog > datos.json

# 2. Descargar (Files tab) o copiar contenido

# 3. En local
cd /Users/prueba/Desktop/me_backend
source venv/bin/activate
python manage.py loaddata datos.json
```

---

## 🛠️ COMANDOS ÚTILES

### Ver shell interactivo:
```bash
python manage.py shell
```

### Crear superusuario local:
```bash
python manage.py createsuperuser
```

### Ver admin local:
```bash
python manage.py runserver
```
Accede a: http://127.0.0.1:8000/admin/

### Aplicar migraciones:
```bash
python manage.py migrate
```

### Ver rutas disponibles:
```bash
python manage.py show_urls  # Si tienes django-extensions
```

---

## 🎯 FLUJO DE TRABAJO RECOMENDADO

1. **Desarrollar localmente:**
   ```bash
   python manage.py runserver
   ```

2. **Probar cambios localmente:**
   - Admin: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/skills/

3. **Hacer commit de código:**
   ```bash
   git add .
   git commit -m "Descripción"
   git push
   ```

4. **Actualizar PythonAnywhere:**
   ```bash
   cd ~/me_backend
   workon portfolio_env
   git pull
   python manage.py migrate
   ```
   Web tab → Reload

---

## ⚠️ IMPORTANTE

- La BD local (SQLite) es diferente a la de PythonAnywhere (MySQL)
- Los cambios en el código SÍ se sincronizan (Git)
- Los cambios en datos NO se sincronizan automáticamente
- Las imágenes en `/media/` son solo locales

---

## 🐛 TROUBLESHOOTING

### Error: `No module named 'decouple'`
```bash
pip install python-decouple
```

### Error: `django.db.utils.OperationalError`
```bash
python manage.py migrate
```

### Error: Puerto 8000 en uso
```bash
python manage.py runserver 8001
```

### Ver logs detallados:
```bash
python manage.py runserver --verbosity 3
```

