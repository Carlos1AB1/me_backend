# 🚀 INICIO RÁPIDO - Desarrollo Local Completo

## 📋 RESUMEN

Tienes **2 servidores** que correr:

1. **Backend Django** → `http://127.0.0.1:8000`
2. **Frontend Next.js** → `http://localhost:3000`

---

## 🎯 COMANDOS RÁPIDOS

### **Terminal 1: Backend Django**

```bash
cd /Users/prueba/Desktop/me_backend
python3 manage.py runserver
```

**✅ Listo cuando veas:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

---

### **Terminal 2: Frontend Next.js**

```bash
cd /Users/prueba/Desktop/me_backend/me
npm run dev
```

**✅ Listo cuando veas:**
```
  ▲ Next.js 14.0.4
  - Local:        http://localhost:3000
  ✓ Ready in 2.3s
```

---

### **Navegador:**

Abre: **http://localhost:3000**

---

## 🔧 CONFIGURACIÓN ACTUAL

### **Backend:**
- ✅ Base de datos: SQLite (`db.sqlite3`)
- ✅ 8 Skills, 2 Projects, 4 Services
- ✅ Admin: http://127.0.0.1:8000/admin/

### **Frontend:**
- ✅ Configurado para usar backend local
- ✅ API URL: `http://127.0.0.1:8000`
- ✅ Hot reload activado

---

## 📊 VER DATOS DEL BACKEND

```bash
cd /Users/prueba/Desktop/me_backend
python3 ver_datos_bd.py
```

---

## 🎨 ADMIN LOCAL

1. Ve a: http://127.0.0.1:8000/admin/
2. Usuario: `admin` o `CarlosArturo`
3. Puedes editar Skills, Projects, Services

---

## 🔄 FLUJO DE TRABAJO

```
1. Terminal 1: python3 manage.py runserver
   ↓
2. Terminal 2: npm run dev
   ↓
3. Navegador: http://localhost:3000
   ↓
4. Editar código → Se actualiza automáticamente
```

---

## ⚠️ IMPORTANTE

- **Backend debe estar corriendo ANTES** de abrir el frontend
- Si cambias algo en el backend, espera unos segundos
- Si cambias algo en el frontend, se actualiza instantáneamente

---

## 🐛 SI ALGO FALLA

### Backend no inicia:
```bash
python3 manage.py migrate
```

### Frontend no inicia:
```bash
cd /Users/prueba/Desktop/me_backend/me
rm -rf node_modules
npm install
```

### No se conectan:
- Verifica que ambos estén corriendo
- Revisa la consola del navegador (F12)
- Verifica que `me/lib/api.ts` tenga: `http://127.0.0.1:8000`

---

## ✅ TODO LISTO

Ahora puedes desarrollar localmente con ambos servidores. 🎉

