from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from skills.models import SkillCategory, Skill
from projects.models import Project
from blog.models import Category, BlogPost
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Carga datos de ejemplo para el portafolio'

    def handle(self, *args, **options):
        # Crear o obtener superusuario
        admin_user, created = User.objects.get_or_create(
            email='admin@portfolio.com',
            defaults={
                'username': 'admin',
                'first_name': 'Carlos',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # Crear categorías de habilidades
        categories_data = [
            {
                'name': 'Frontend Development',
                'description': 'Creación de interfaces modernas y responsivas',
                'icon': '💻',
                'order': 1
            },
            {
                'name': 'Backend Development',
                'description': 'APIs robustas y arquitecturas escalables',
                'icon': '⚙️',
                'order': 2
            },
            {
                'name': 'Database & Cloud',
                'description': 'Gestión de datos y infraestructura en la nube',
                'icon': '☁️',
                'order': 3
            },
            {
                'name': 'Mobile & Tools',
                'description': 'Desarrollo móvil y herramientas de productividad',
                'icon': '📱',
                'order': 4
            }
        ]

        for cat_data in categories_data:
            category, created = SkillCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Categoría creada: {category.name}')

        # Crear habilidades
        skills_data = [
            # Frontend
            {'name': 'React', 'category': 'Frontend Development', 'level': 'Experto', 'icon': '⚛️', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg', 'is_featured': True},
            {'name': 'Next.js', 'category': 'Frontend Development', 'level': 'Experto', 'icon': '🚀', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg', 'is_featured': True},
            {'name': 'TypeScript', 'category': 'Frontend Development', 'level': 'Experto', 'icon': '📘', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg', 'is_featured': True},
            {'name': 'Vue.js', 'category': 'Frontend Development', 'level': 'Intermedio', 'icon': '💚', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg'},
            
            # Backend
            {'name': 'Node.js', 'category': 'Backend Development', 'level': 'Experto', 'icon': '🟢', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg', 'is_featured': True},
            {'name': 'Python', 'category': 'Backend Development', 'level': 'Experto', 'icon': '🐍', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg', 'is_featured': True},
            {'name': 'Django', 'category': 'Backend Development', 'level': 'Intermedio', 'icon': '🎯'},
            
            # Database & Cloud
            {'name': 'MongoDB', 'category': 'Database & Cloud', 'level': 'Experto', 'icon': '🍃', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg', 'is_featured': True},
            {'name': 'AWS', 'category': 'Database & Cloud', 'level': 'Intermedio', 'icon': '☁️', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg', 'is_featured': True},
            {'name': 'Docker', 'category': 'Database & Cloud', 'level': 'Intermedio', 'icon': '🐳', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg', 'is_featured': True},
            
            # Tools
            {'name': 'Git', 'category': 'Mobile & Tools', 'level': 'Experto', 'icon': '📋', 'image_url': 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg', 'is_featured': True},
        ]

        for skill_data in skills_data:
            category = SkillCategory.objects.get(name=skill_data.pop('category'))
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                category=category,
                defaults={**skill_data, 'category': category}
            )
            if created:
                self.stdout.write(f'Habilidad creada: {skill.name}')

        # Crear categorías de blog
        blog_categories = [
            {'name': 'Web Development', 'slug': 'web-development', 'color': '#007bff'},
            {'name': 'JavaScript', 'slug': 'javascript', 'color': '#28a745'},
            {'name': 'Python', 'slug': 'python', 'color': '#ffc107'},
            {'name': 'Tutorials', 'slug': 'tutorials', 'color': '#dc3545'},
        ]

        for cat_data in blog_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Categoría de blog creada: {category.name}')

        # Crear proyectos de ejemplo
        projects_data = [
            {
                'title': 'Portafolio Personal',
                'slug': 'portfolio-personal',
                'description': 'Un portafolio moderno desarrollado con Next.js y Django REST Framework, featuring animaciones avanzadas y un backend robusto.',
                'short_description': 'Portafolio personal con Next.js y Django',
                'technologies': 'Next.js, React, TypeScript, Django, PostgreSQL, AWS',
                'github_url': 'https://github.com/usuario/portfolio',
                'live_url': 'https://portfolio.ejemplo.com',
                'priority': 3,
                'status': 'published',
                'featured': True,
                'start_date': timezone.now().date() - timedelta(days=60),
                'end_date': timezone.now().date() - timedelta(days=30),
            },
            {
                'title': 'E-commerce Dashboard',
                'slug': 'ecommerce-dashboard',
                'description': 'Dashboard administrativo completo para e-commerce con gestión de productos, órdenes y analytics en tiempo real.',
                'short_description': 'Dashboard para e-commerce con analytics',
                'technologies': 'React, Node.js, MongoDB, Redis, Chart.js',
                'github_url': 'https://github.com/usuario/ecommerce-dashboard',
                'priority': 2,
                'status': 'published',
                'featured': True,
                'start_date': timezone.now().date() - timedelta(days=90),
                'end_date': timezone.now().date() - timedelta(days=45),
            }
        ]

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=project_data['title'],
                defaults={**project_data, 'created_by': admin_user}
            )
            if created:
                self.stdout.write(f'Proyecto creado: {project.title}')

        self.stdout.write(
            self.style.SUCCESS('Datos de ejemplo cargados exitosamente!')
        )
