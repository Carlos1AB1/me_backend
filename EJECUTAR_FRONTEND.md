# 🎨 Ejecutar Frontend Localmente

## 🚀 PASOS RÁPIDOS

### 1️⃣ Instalar dependencias (solo la primera vez)

```bash
cd /Users/prueba/Desktop/me_backend/me
npm install
```

### 2️⃣ Ejecutar servidor de desarrollo

```bash
npm run dev
```

### 3️⃣ Abrir en el navegador

```
http://localhost:3000
```

---

## 🔧 CONFIGURACIÓN

### **Backend Local (Recomendado para desarrollo):**

El frontend está configurado para usar el backend local por defecto:

```typescript
// me/lib/api.ts
const API_BASE_URL = 'http://127.0.0.1:8000';
```

**Requisitos:**
- ✅ Backend Django debe estar corriendo en `http://127.0.0.1:8000`
- ✅ Ejecuta: `python3 manage.py runserver` (en otra terminal)

---

### **Backend de Producción (PythonAnywhere):**

Si quieres usar el backend de producción, edita `me/lib/api.ts`:

```typescript
const API_BASE_URL = 'https://cabaron23.pythonanywhere.com';
```

O usa variable de entorno:

```bash
NEXT_PUBLIC_API_URL=https://cabaron23.pythonanywhere.com npm run dev
```

---

## 📋 FLUJO COMPLETO DE DESARROLLO

### **Terminal 1: Backend Django**

```bash
cd /Users/prueba/Desktop/me_backend
python3 manage.py runserver
```

**Salida esperada:**
```
Starting development server at http://127.0.0.1:8000/
```

---

### **Terminal 2: Frontend Next.js**

```bash
cd /Users/prueba/Desktop/me_backend/me
npm run dev
```

**Salida esperada:**
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
  - ready started server on 0.0.0.0:3000
```

---

### **Navegador:**

1. Abre: http://localhost:3000
2. El frontend se conectará automáticamente al backend local
3. Verás tus Skills, Projects, Services, etc.

---

## 🛠️ COMANDOS ÚTILES

### **Instalar dependencias:**
```bash
npm install
```

### **Ejecutar en desarrollo:**
```bash
npm run dev
```

### **Build para producción:**
```bash
npm run build
```

### **Ejecutar build de producción:**
```bash
npm start
```

### **Linter:**
```bash
npm run lint
```

---

## 🔍 VERIFICAR CONEXIÓN

### **1. Verificar que el backend responde:**

```bash
curl http://127.0.0.1:8000/api/skills/
```

Debe devolver JSON con tus skills.

---

### **2. Verificar en el navegador:**

1. Abre: http://localhost:3000
2. Abre DevTools (F12)
3. Ve a la pestaña **Network**
4. Recarga la página
5. Busca requests a `http://127.0.0.1:8000`
6. Deben ser **200 OK** ✅

---

## 🐛 TROUBLESHOOTING

### ❌ **Error: "Cannot find module"**

```bash
cd /Users/prueba/Desktop/me_backend/me
rm -rf node_modules package-lock.json
npm install
```

---

### ❌ **Error: "Port 3000 already in use"**

```bash
# Opción 1: Matar proceso en puerto 3000
lsof -ti:3000 | xargs kill -9

# Opción 2: Usar otro puerto
PORT=3001 npm run dev
```

---

### ❌ **Error: "ECONNREFUSED" al conectar al backend**

**Causa:** El backend Django no está corriendo.

**Solución:**
```bash
# En otra terminal
cd /Users/prueba/Desktop/me_backend
python3 manage.py runserver
```

---

### ❌ **Error: CORS en el navegador**

**Causa:** El backend no permite requests desde `localhost:3000`.

**Solución:** Verifica que en `portfolio_backend/settings.py` esté:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

### ❌ **Las imágenes no cargan**

**Causa:** Las URLs de imágenes son relativas o apuntan a PythonAnywhere.

**Solución:**
1. Verifica que el backend local tenga las imágenes en `/media/`
2. O usa URLs absolutas de GitHub/ImgBB
3. O cambia temporalmente `api.ts` para usar PythonAnywhere

---

## 📊 ESTRUCTURA DEL PROYECTO

```
me_backend/
├── portfolio_backend/     ← Backend Django
│   └── settings.py
│
└── me/                    ← Frontend Next.js
    ├── app/
    ├── components/
    ├── lib/
    │   └── api.ts         ← Configuración de API
    └── package.json
```

---

## 🎯 VARIABLES DE ENTORNO

Crea un archivo `.env.local` en `me/`:

```bash
cd /Users/prueba/Desktop/me_backend/me
touch .env.local
```

Contenido:

```env
# Backend local
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# O backend de producción
# NEXT_PUBLIC_API_URL=https://cabaron23.pythonanywhere.com
```

---

## ✅ CHECKLIST

- [ ] Node.js instalado (`node --version`)
- [ ] Dependencias instaladas (`npm install`)
- [ ] Backend Django corriendo (`python3 manage.py runserver`)
- [ ] Frontend corriendo (`npm run dev`)
- [ ] Navegador abierto en `http://localhost:3000`
- [ ] DevTools abierto para ver errores
- [ ] Network tab muestra requests exitosos

---

## 🚀 COMANDO TODO-EN-UNO

```bash
# Terminal 1: Backend
cd /Users/prueba/Desktop/me_backend && python3 manage.py runserver

# Terminal 2: Frontend
cd /Users/prueba/Desktop/me_backend/me && npm run dev
```

---

## 📝 NOTAS

- El frontend usa **Hot Reload**: Los cambios se reflejan automáticamente
- El backend también tiene **Auto-reload**: Reinicia automáticamente
- Para ver cambios en el backend, espera unos segundos
- Para ver cambios en el frontend, se actualizan instantáneamente

---

**¡Listo! Ahora puedes desarrollar localmente con ambos servidores corriendo.** 🎉

