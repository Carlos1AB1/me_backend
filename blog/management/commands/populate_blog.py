from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Category, BlogPost
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate blog with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating blog categories...')
        
        # Crear o obtener un usuario para los posts
        try:
            author = User.objects.filter(is_superuser=True).first()
            if not author:
                author = User.objects.create_user(
                    email='admin@example.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True
                )
                self.stdout.write('Created admin user for blog posts')
            else:
                self.stdout.write(f'Using existing admin user: {author.email}')
        except Exception as e:
            self.stdout.write(f'Error getting user: {e}')

        # Crear categorías
        categories_data = [
            {
                'name': 'Desarrollo Web',
                'description': 'Artículos sobre desarrollo web, frameworks y tecnologías frontend/backend',
                'color': '#3b82f6'
            },
            {
                'name': 'JavaScript',
                'description': 'Todo sobre JavaScript, ES6+, Node.js y el ecosistema JS',
                'color': '#f59e0b'
            },
            {
                'name': 'React & Next.js',
                'description': 'Tutoriales y tips sobre React, Next.js y desarrollo frontend moderno',
                'color': '#06b6d4'
            },
            {
                'name': 'Backend & APIs',
                'description': 'Desarrollo de APIs, bases de datos y arquitectura backend',
                'color': '#10b981'
            },
            {
                'name': 'Carrera Tech',
                'description': 'Consejos para developers, carrera profesional y industria tech',
                'color': '#8b5cf6'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Crear posts del blog
        posts_data = [
            {
                'title': 'Guía Completa de Next.js 14: App Router y Server Components',
                'excerpt': 'Descubre las nuevas características de Next.js 14, incluyendo App Router, Server Components y las mejores prácticas para desarrollo moderno.',
                'content': '''# Guía Completa de Next.js 14

Next.js 14 ha llegado con importantes mejoras y nuevas características que revolucionan el desarrollo web moderno. En este artículo exploraremos las principales novedades y cómo implementarlas en tus proyectos.

## App Router: El Nuevo Paradigma

El App Router de Next.js 13/14 introduce un nuevo modelo de routing basado en el sistema de archivos, pero con capacidades mejoradas:

### Características Principales:
- **Layouts anidados**: Reutiliza componentes de layout en diferentes niveles
- **Loading UI**: Estados de carga automáticos para mejor UX
- **Error Handling**: Manejo de errores más granular
- **Parallel Routes**: Renderiza múltiples páginas simultáneamente

## Server Components por Defecto

Los Server Components son ahora el comportamiento por defecto en el App Router:

```javascript
// Este componente se renderiza en el servidor
export default async function BlogPost({ params }) {
  const post = await fetchPost(params.id);
  return <article>{post.content}</article>;
}
```

### Ventajas de los Server Components:
- Mejor rendimiento inicial
- Menor bundle size del cliente
- Acceso directo a recursos del servidor
- SEO mejorado

## Streaming y Suspense

Next.js 14 mejora el streaming de contenido:

```javascript
import { Suspense } from 'react';

export default function Page() {
  return (
    <Suspense fallback={<Loading />}>
      <SlowComponent />
    </Suspense>
  );
}
```

## Conclusión

Next.js 14 representa un gran salto hacia adelante en el desarrollo web moderno. La combinación de App Router, Server Components y las mejoras en streaming hacen que sea más fácil que nunca crear aplicaciones rápidas y escalables.

¿Has migrado ya a Next.js 14? ¡Comparte tu experiencia en los comentarios!''',
                'categories': ['Desarrollo Web', 'React & Next.js'],
                'tags': 'Next.js, React, Server Components, App Router, Web Development',
                'is_featured': True,
                'read_time': 8,
                'status': 'published',
                'published_at': timezone.now() - timezone.timedelta(days=2)
            },
            {
                'title': 'TypeScript para Principiantes: De Cero a Héroe',
                'excerpt': 'Aprende TypeScript desde cero con ejemplos prácticos. Descubre por qué TypeScript es esencial para el desarrollo moderno de JavaScript.',
                'content': '''# TypeScript para Principiantes

TypeScript se ha convertido en el estándar de facto para el desarrollo de JavaScript a gran escala. En esta guía aprenderás todo lo necesario para empezar.

## ¿Qué es TypeScript?

TypeScript es un superset de JavaScript que añade tipado estático opcional. Esto significa que puedes escribir JavaScript normal, pero con la ventaja de tener tipos que te ayudan a detectar errores temprano.

### Ventajas de TypeScript:
- **Detección temprana de errores**: Los tipos ayudan a encontrar bugs antes de ejecutar el código
- **Mejor IntelliSense**: Autocompletado más inteligente en tu editor
- **Refactoring seguro**: Cambios de código más confiables
- **Documentación viva**: Los tipos sirven como documentación

## Tipos Básicos

```typescript
// Tipos primitivos
let nombre: string = "Juan";
let edad: number = 25;
let activo: boolean = true;

// Arrays
let numeros: number[] = [1, 2, 3, 4, 5];
let frutas: Array<string> = ["manzana", "banana"];

// Objetos
interface Usuario {
  id: number;
  nombre: string;
  email: string;
  activo?: boolean; // Propiedad opcional
}

const usuario: Usuario = {
  id: 1,
  nombre: "Ana",
  email: "ana@example.com"
};
```

## Funciones Tipadas

```typescript
function sumar(a: number, b: number): number {
  return a + b;
}

// Función con parámetros opcionales
function saludar(nombre: string, apellido?: string): string {
  return apellido ? `Hola ${nombre} ${apellido}` : `Hola ${nombre}`;
}

// Arrow functions
const multiplicar = (a: number, b: number): number => a * b;
```

## Interfaces y Tipos

```typescript
// Interface
interface Producto {
  id: number;
  nombre: string;
  precio: number;
  categoria: string;
}

// Type alias
type Estado = "pendiente" | "completado" | "cancelado";

// Extendiendo interfaces
interface ProductoConDescuento extends Producto {
  descuento: number;
}
```

## Conclusión

TypeScript no es solo una moda pasajera, es una herramienta que mejora significativamente la experiencia de desarrollo y la calidad del código. Empieza poco a poco agregando tipos a tu código JavaScript existente.

¡El futuro del desarrollo web es tipado!''',
                'categories': ['JavaScript', 'Desarrollo Web'],
                'tags': 'TypeScript, JavaScript, Types, Programming, Web Development',
                'is_featured': True,
                'read_time': 10,
                'status': 'published',
                'published_at': timezone.now() - timezone.timedelta(days=5)
            },
            {
                'title': 'Construyendo APIs RESTful con Node.js y Express',
                'excerpt': 'Aprende a crear APIs robustas y escalables usando Node.js, Express y mejores prácticas de desarrollo backend.',
                'content': '''# Construyendo APIs RESTful con Node.js y Express

Crear APIs bien estructuradas es fundamental para cualquier aplicación moderna. En este tutorial aprenderás a construir APIs RESTful robustas con Node.js y Express.

## Configuración Inicial

Primero, configuremos nuestro proyecto:

```bash
mkdir mi-api
cd mi-api
npm init -y
npm install express cors helmet morgan dotenv
npm install -D nodemon @types/node
```

## Estructura del Proyecto

```
mi-api/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   └── app.js
├── .env
└── server.js
```

## Configuración Básica de Express

```javascript
// src/app.js
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const app = express();

// Middleware de seguridad
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Rutas
app.use('/api/v1/users', require('./routes/users'));
app.use('/api/v1/posts', require('./routes/posts'));

// Manejo de errores
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: 'Algo salió mal!' });
});

module.exports = app;
```

## Creando Controladores

```javascript
// src/controllers/userController.js
const users = []; // En producción usarías una base de datos

const getUsers = (req, res) => {
  res.json({
    success: true,
    data: users,
    count: users.length
  });
};

const createUser = (req, res) => {
  const { name, email } = req.body;
  
  if (!name || !email) {
    return res.status(400).json({
      success: false,
      message: 'Nombre y email son requeridos'
    });
  }

  const newUser = {
    id: Date.now(),
    name,
    email,
    createdAt: new Date()
  };

  users.push(newUser);
  
  res.status(201).json({
    success: true,
    data: newUser
  });
};

module.exports = {
  getUsers,
  createUser
};
```

## Definiendo Rutas

```javascript
// src/routes/users.js
const express = require('express');
const { getUsers, createUser } = require('../controllers/userController');
const router = express.Router();

router.get('/', getUsers);
router.post('/', createUser);

module.exports = router;
```

## Middleware de Validación

```javascript
// src/middleware/validation.js
const validateUser = (req, res, next) => {
  const { name, email } = req.body;
  
  if (!name || name.length < 2) {
    return res.status(400).json({
      success: false,
      message: 'El nombre debe tener al menos 2 caracteres'
    });
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailRegex.test(email)) {
    return res.status(400).json({
      success: false,
      message: 'Email inválido'
    });
  }

  next();
};

module.exports = { validateUser };
```

## Mejores Prácticas

### 1. Códigos de Estado HTTP Apropiados
- 200: OK
- 201: Creado
- 400: Bad Request
- 401: No autorizado
- 404: No encontrado
- 500: Error del servidor

### 2. Estructura de Respuesta Consistente
```javascript
{
  "success": true,
  "data": {...},
  "message": "Operación exitosa"
}
```

### 3. Manejo de Errores Centralizado
```javascript
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}
```

## Conclusión

Construir APIs RESTful bien estructuradas requiere planificación y seguir mejores prácticas. Con Express.js tienes todas las herramientas necesarias para crear APIs robustas y escalables.

¡Empieza a construir tu próxima API siguiendo estos patrones!''',
                'categories': ['Backend & APIs', 'JavaScript'],
                'tags': 'Node.js, Express, API, REST, Backend, JavaScript',
                'is_featured': True,
                'read_time': 12,
                'status': 'published',
                'published_at': timezone.now() - timezone.timedelta(days=7)
            },
            {
                'title': '5 Consejos para Acelerar tu Carrera como Developer',
                'excerpt': 'Estrategias probadas para impulsar tu carrera en tecnología y destacar en el competitivo mundo del desarrollo de software.',
                'content': '''# 5 Consejos para Acelerar tu Carrera como Developer

La industria tecnológica evoluciona constantemente, y mantenerse relevante requiere estrategia y dedicación. Aquí tienes 5 consejos probados para acelerar tu carrera.

## 1. Construye un Portfolio Sólido

Tu portfolio es tu carta de presentación. No basta con tener proyectos; necesitas proyectos que cuenten una historia.

### Qué incluir:
- **3-5 proyectos diversos**: Muestra diferentes tecnologías y tipos de proyectos
- **Código limpio y documentado**: GitHub con README detallados
- **Proyectos desplegados**: Usa Vercel, Netlify o Heroku
- **Casos de estudio**: Explica el problema, solución y tecnologías usadas

### Ejemplo de estructura:
```
Portfolio/
├── E-commerce Full Stack
├── App Móvil React Native
├── Dashboard con D3.js
└── API REST con autenticación
```

## 2. Contribuye a Open Source

El open source es una excelente manera de:
- Mejorar tus habilidades de programación
- Trabajar con desarrolladores experimentados
- Construir tu reputación en la comunidad
- Aprender sobre proyectos a gran escala

### Cómo empezar:
1. Busca proyectos con el tag "good first issue"
2. Lee la documentación del proyecto
3. Empieza con correcciones pequeñas
4. Gradualmente toma tareas más complejas

## 3. Especialízate en una Tecnología

Aunque es bueno conocer varias tecnologías, especialízarte en una te dará ventaja competitiva.

### Tecnologías con alta demanda:
- **Frontend**: React, Vue.js, Angular
- **Backend**: Node.js, Python (Django/FastAPI), Go
- **Mobile**: React Native, Flutter
- **Cloud**: AWS, Azure, GCP
- **DevOps**: Docker, Kubernetes, CI/CD

### Cómo especializarte:
- Dedica 80% de tu tiempo a tu especialidad
- Certifícate en esa tecnología
- Participa en comunidades específicas
- Escribe sobre tu especialidad

## 4. Desarrolla Habilidades Blandas

Las habilidades técnicas te pueden conseguir una entrevista, pero las habilidades blandas te conseguirán el trabajo.

### Habilidades clave:
- **Comunicación**: Explica conceptos técnicos de forma simple
- **Trabajo en equipo**: Colabora efectivamente en proyectos
- **Resolución de problemas**: Enfócate en soluciones, no en problemas
- **Adaptabilidad**: Abraza el cambio y nuevas tecnologías
- **Liderazgo**: Toma iniciativa en proyectos

### Cómo desarrollarlas:
- Participa en meetups y conferencias
- Presenta tus proyectos públicamente
- Mentoriza a otros developers
- Practica explicar código a no-técnicos

## 5. Construye tu Red de Contactos

Tu red profesional es uno de tus activos más valiosos. Muchas oportunidades llegan a través de contactos.

### Estrategias de networking:
- **Twitter Tech**: Sigue y participa en conversaciones
- **LinkedIn**: Mantén tu perfil actualizado y comparte contenido
- **Eventos locales**: Asiste a meetups y conferencias
- **Discord/Slack**: Únete a comunidades de developers
- **Mentorías**: Tanto ser mentor como tener mentores

### Template de mensaje en LinkedIn:
```
Hola [Nombre],

Vi tu experiencia en [Empresa/Proyecto] y me parece fascinante tu trabajo en [tecnología específica]. 

Soy developer especializado en [tu especialidad] y me encantaría conectar contigo para intercambiar experiencias sobre [tema común].

¡Saludos!
```

## Bonus: Mantente Actualizado

La tecnología cambia rápidamente. Mantente al día:
- **Newsletters**: JavaScript Weekly, React Status
- **Podcasts**: Syntax, The Changelog
- **YouTube**: Canales técnicos de calidad
- **Documentación oficial**: Siempre la fuente más confiable

## Conclusión

Acelerar tu carrera como developer requiere ser intencional y consistente. No intentes hacer todo a la vez; elige 1-2 áreas y enfócate en mejorar constantemente.

Recuerda: la programación es un maratón, no un sprint. La consistencia vence a la intensidad.

¡Tu carrera tech te está esperando!''',
                'categories': ['Carrera Tech'],
                'tags': 'Career, Programming, Professional Development, Tech Industry, Skills',
                'is_featured': False,
                'read_time': 6,
                'status': 'published',
                'published_at': timezone.now() - timezone.timedelta(days=10)
            },
            {
                'title': 'React Hooks Avanzados: useCallback, useMemo y useRef',
                'excerpt': 'Domina los hooks avanzados de React para optimizar el rendimiento y crear componentes más eficientes.',
                'content': '''# React Hooks Avanzados: useCallback, useMemo y useRef

Los hooks básicos como useState y useEffect son fundamentales, pero para crear aplicaciones React verdaderamente optimizadas, necesitas dominar los hooks avanzados.

## useCallback: Memorizando Funciones

useCallback memoriza una función y solo la recrea cuando sus dependencias cambian.

### Cuándo usarlo:
- Cuando pasas funciones como props a componentes hijos
- Para evitar re-renders innecesarios
- En efectos que dependen de funciones

```javascript
import React, { useState, useCallback } from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [filter, setFilter] = useState('all');

  // ❌ Malo: Se crea una nueva función en cada render
  const addTodo = (text) => {
    setTodos(prev => [...prev, { id: Date.now(), text, completed: false }]);
  };

  // ✅ Bueno: Función memorizada
  const addTodoMemoized = useCallback((text) => {
    setTodos(prev => [...prev, { id: Date.now(), text, completed: false }]);
  }, []); // Sin dependencias

  const toggleTodo = useCallback((id) => {
    setTodos(prev => prev.map(todo => 
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  }, []);

  return (
    <div>
      <TodoForm onSubmit={addTodoMemoized} />
      <TodoList todos={todos} onToggle={toggleTodo} />
    </div>
  );
}
```

### Ejemplo Práctico con React.memo:

```javascript
const TodoItem = React.memo(({ todo, onToggle }) => {
  console.log(`Rendering todo: ${todo.text}`);
  
  return (
    <div onClick={() => onToggle(todo.id)}>
      {todo.text} {todo.completed ? '✅' : '⭕'}
    </div>
  );
});

// Sin useCallback, TodoItem se re-renderiza aunque no haya cambiado
// Con useCallback, solo se re-renderiza cuando es necesario
```

## useMemo: Memorizando Valores Calculados

useMemo memoriza el resultado de una computación costosa.

### Cuándo usarlo:
- Cálculos complejos o costosos
- Filtros y transformaciones de arrays grandes
- Crear objetos/arrays que se pasan como props

```javascript
import React, { useState, useMemo } from 'react';

function ExpensiveComponent({ items, searchTerm }) {
  const [sortOrder, setSortOrder] = useState('asc');

  // ❌ Malo: Se ejecuta en cada render
  const filteredAndSortedItems = items
    .filter(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => {
      if (sortOrder === 'asc') {
        return a.name.localeCompare(b.name);
      }
      return b.name.localeCompare(a.name);
    });

  // ✅ Bueno: Solo se recalcula cuando cambian las dependencias
  const filteredAndSortedItemsMemo = useMemo(() => {
    console.log('Calculating filtered and sorted items...');
    
    return items
      .filter(item => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
      .sort((a, b) => {
        if (sortOrder === 'asc') {
          return a.name.localeCompare(b.name);
        }
        return b.name.localeCompare(a.name);
      });
  }, [items, searchTerm, sortOrder]);

  return (
    <div>
      <button onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}>
        Sort {sortOrder === 'asc' ? 'Descending' : 'Ascending'}
      </button>
      {filteredAndSortedItemsMemo.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
}
```

### Ejemplo con Objetos:

```javascript
function UserProfile({ user, permissions }) {
  // ✅ Memorizar objetos que se pasan como props
  const userPermissions = useMemo(() => ({
    canEdit: permissions.includes('edit'),
    canDelete: permissions.includes('delete'),
    canShare: permissions.includes('share')
  }), [permissions]);

  return <UserActions user={user} permissions={userPermissions} />;
}
```

## useRef: Referencias Mutables

useRef te da una referencia mutable que persiste durante toda la vida del componente.

### Casos de uso comunes:

#### 1. Acceder a elementos del DOM:

```javascript
import React, { useRef, useEffect } from 'react';

function FocusInput() {
  const inputRef = useRef(null);

  useEffect(() => {
    // Enfocar el input cuando el componente se monta
    inputRef.current.focus();
  }, []);

  const handleClick = () => {
    inputRef.current.focus();
  };

  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={handleClick}>Focus Input</button>
    </div>
  );
}
```

#### 2. Almacenar valores mutables:

```javascript
function Timer() {
  const [count, setCount] = useState(0);
  const intervalRef = useRef(null);

  const startTimer = () => {
    if (intervalRef.current) return; // Ya está corriendo
    
    intervalRef.current = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);
  };

  const stopTimer = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return (
    <div>
      <h1>{count}</h1>
      <button onClick={startTimer}>Start</button>
      <button onClick={stopTimer}>Stop</button>
    </div>
  );
}
```

#### 3. Valores previos:

```javascript
function usePrevious(value) {
  const ref = useRef();
  
  useEffect(() => {
    ref.current = value;
  });
  
  return ref.current;
}

function Counter() {
  const [count, setCount] = useState(0);
  const prevCount = usePrevious(count);

  return (
    <div>
      <h1>Current: {count}</h1>
      <h2>Previous: {prevCount}</h2>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

## Errores Comunes y Cómo Evitarlos

### 1. Sobre-optimización con useCallback/useMemo:

```javascript
// ❌ Innecesario: valores primitivos son baratos de comparar
const memoizedNumber = useMemo(() => 42, []);

// ❌ Innecesario: cálculos simples
const doubled = useMemo(() => count * 2, [count]);

// ✅ Necesario: cálculos costosos
const expensiveValue = useMemo(() => {
  return items.reduce((acc, item) => {
    return acc + complexCalculation(item);
  }, 0);
}, [items]);
```

### 2. Dependencias incorrectas:

```javascript
// ❌ Malo: falta dependencia
const fetchData = useCallback(() => {
  fetch(`/api/users/${userId}`);
}, []); // userId debería estar en las dependencias

// ✅ Bueno: dependencias correctas
const fetchData = useCallback(() => {
  fetch(`/api/users/${userId}`);
}, [userId]);
```

## Conclusión

Los hooks avanzados son herramientas poderosas para optimizar el rendimiento de tus aplicaciones React:

- **useCallback**: Memoriza funciones para evitar re-renders
- **useMemo**: Memoriza valores calculados costosos
- **useRef**: Accede al DOM y mantiene valores mutables

Recuerda: la optimización prematura es la raíz de todos los males. Usa estos hooks cuando realmente los necesites, no por defecto.

¡Mide primero, optimiza después!''',
                'categories': ['React & Next.js', 'JavaScript'],
                'tags': 'React, Hooks, Performance, useCallback, useMemo, useRef, Optimization',
                'is_featured': False,
                'read_time': 9,
                'status': 'published',
                'published_at': timezone.now() - timezone.timedelta(days=14)
            }
        ]

        # Crear posts
        for post_data in posts_data:
            # Extraer categorías
            post_categories = post_data.pop('categories')
            
            # Crear el post
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    **post_data,
                    'author': author
                }
            )
            
            if created:
                # Agregar categorías
                for cat_name in post_categories:
                    if cat_name in categories:
                        post.categories.add(categories[cat_name])
                
                self.stdout.write(f'Created post: {post.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated blog!')
        )
