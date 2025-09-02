# Portfolio Backend - Django REST API

Backend completo desarrollado con Django 4.2 y Django REST Framework para el portafolio personal. Incluye autenticación JWT, CRUD completo, documentación con Swagger y todas las funcionalidades necesarias para el frontend de Next.js.

## 🚀 Características

- **Autenticación JWT** con refresh tokens
- **API REST completa** para todas las entidades
- **Documentación automática** con Swagger/OpenAPI
- **Sistema de permisos** granular
- **Paginación** y filtros avanzados
- **Subida de archivos** para imágenes y media
- **Admin panel** personalizado
- **CORS** configurado para frontend
- **Validaciones** robustas
- **Logging** y manejo de errores

## 📋 Requisitos

- Python 3.11+
- pip
- virtualenv (recomendado)

## 🛠️ Instalación

### 1. Clonar y configurar entorno

```bash
# Navegar al directorio del backend
cd portfolio_backend

# Activar entorno virtual (ya creado)
source ../backend_env/bin/activate

# Las dependencias ya están instaladas, pero si necesitas reinstalar:
# pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar variables según necesidades
nano .env
```

### 3. Ejecutar migraciones

```bash
# Las migraciones ya están aplicadas, pero si necesitas reaplicar:
python manage.py migrate
```

### 4. Crear superusuario (opcional, ya existe uno)

```bash
python manage.py createsuperuser
```

### 5. Cargar datos de ejemplo

```bash
python manage.py load_sample_data
```

### 6. Ejecutar servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## 📊 Endpoints principales

### Autenticación
- `POST /api/v1/auth/register/` - Registro de usuarios
- `POST /api/v1/auth/login/` - Login
- `POST /api/v1/auth/logout/` - Logout
- `GET /api/v1/auth/profile/` - Perfil del usuario
- `PUT /api/v1/auth/profile/` - Actualizar perfil
- `POST /api/v1/auth/change-password/` - Cambiar contraseña
- `POST /api/v1/auth/token/refresh/` - Refresh token

### Proyectos
- `GET /api/v1/projects/` - Listar proyectos
- `POST /api/v1/projects/` - Crear proyecto (auth)
- `GET /api/v1/projects/{id}/` - Detalle de proyecto
- `PUT /api/v1/projects/{id}/` - Actualizar proyecto (auth)
- `DELETE /api/v1/projects/{id}/` - Eliminar proyecto (auth)
- `GET /api/v1/projects/featured/` - Proyectos destacados

### Habilidades
- `GET /api/v1/skills/categories/` - Categorías de habilidades
- `GET /api/v1/skills/` - Listar habilidades
- `GET /api/v1/skills/featured/` - Habilidades destacadas
- `GET /api/v1/skills/by_category/` - Habilidades por categoría

### Blog
- `GET /api/v1/blog/categories/` - Categorías del blog
- `GET /api/v1/blog/` - Listar posts
- `GET /api/v1/blog/{id}/` - Detalle de post
- `GET /api/v1/blog/featured/` - Posts destacados
- `GET /api/v1/blog/recent/` - Posts recientes

### Contacto
- `POST /api/v1/contact/send/` - Enviar mensaje
- `GET /api/v1/contact/messages/` - Listar mensajes (admin)

### Utilidades
- `GET /api/v1/core/health/` - Health check

## 📖 Documentación API

- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`
- **OpenAPI JSON**: `http://127.0.0.1:8000/swagger.json`

## 🔧 Panel de Administración

Accede al panel de admin en: `http://127.0.0.1:8000/admin/`

**Credenciales por defecto:**
- Email: `admin@portfolio.com`
- Password: `admin123` (la que configuraste)

## 🗂️ Estructura del proyecto

```
portfolio_backend/
├── accounts/           # Gestión de usuarios y autenticación
├── blog/              # Posts y categorías del blog
├── contact/           # Mensajes de contacto
├── core/              # Funcionalidades centrales
├── projects/          # Gestión de proyectos
├── skills/            # Habilidades y categorías
├── portfolio_backend/ # Configuración principal
├── static/            # Archivos estáticos
├── media/             # Archivos subidos
├── manage.py          # Script de gestión Django
├── requirements.txt   # Dependencias
├── .env              # Variables de entorno
└── README.md         # Este archivo
```

## 🔒 Autenticación

El sistema usa **JWT (JSON Web Tokens)** con:
- **Access Token**: 60 minutos de duración
- **Refresh Token**: 24 horas de duración
- **Blacklist**: Los tokens se invalidan al logout

### Ejemplo de uso:

```javascript
// Login
const response = await fetch('http://127.0.0.1:8000/api/v1/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const data = await response.json();
const { access, refresh } = data.tokens;

// Usar token en requests autenticados
const projectsResponse = await fetch('http://127.0.0.1:8000/api/v1/projects/', {
  headers: {
    'Authorization': `Bearer ${access}`
  }
});
```

## 🌐 CORS

CORS está configurado para permitir requests desde:
- `http://localhost:3000` (Next.js dev)
- `http://127.0.0.1:3000`

Para añadir más dominios, edita `CORS_ALLOWED_ORIGINS` en `.env`.

## 📝 Filtros y Búsqueda

La API soporta filtros avanzados:

```bash
# Filtrar proyectos por estado
GET /api/v1/projects/?status=published

# Buscar en el contenido
GET /api/v1/blog/?search=javascript

# Ordenar por fecha
GET /api/v1/projects/?ordering=-created_at

# Paginación
GET /api/v1/blog/?page=2&page_size=10
```

## 🚀 Despliegue

### Variables de entorno para producción:

```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-super-segura
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DATABASE_URL=postgresql://user:password@host:5432/database
CORS_ALLOWED_ORIGINS=https://tu-frontend.com
```

### Comandos de despliegue:

```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

## 🔧 Comandos útiles

```bash
# Crear nueva migración
python manage.py makemigrations

# Ver SQL de migración
python manage.py sqlmigrate app_name migration_number

# Shell interactivo
python manage.py shell

# Limpiar base de datos
python manage.py flush

# Cargar datos de ejemplo
python manage.py load_sample_data
```

## 🛡️ Seguridad

- **CSRF** protection habilitado
- **XSS** protection con headers seguros
- **SQL Injection** prevención con ORM
- **Rate limiting** para API calls
- **Validación** robusta en serializers
- **Sanitización** de inputs

## 🐛 Troubleshooting

### Error de CORS
```bash
# Verificar configuración en settings.py
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
```

### Error de migraciones
```bash
# Reset migraciones (¡cuidado en producción!)
python manage.py migrate --fake-initial
```

### Error de permisos de archivos
```bash
# Verificar permisos de media/
chmod 755 media/
```

## 📞 Soporte

Para problemas o preguntas:
1. Revisar la documentación de Swagger
2. Verificar logs del servidor
3. Consultar issues en el repositorio

## 🎯 Próximas mejoras

- [ ] Sistema de notificaciones
- [ ] Cache con Redis
- [ ] Tests automatizados
- [ ] CI/CD pipeline
- [ ] Monitoreo y métricas
- [ ] Backup automático

---

**Desarrollado con ❤️ usando Django REST Framework**
