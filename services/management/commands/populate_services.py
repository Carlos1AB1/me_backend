from django.core.management.base import BaseCommand
from services.models import ServiceCategory, Service

class Command(BaseCommand):
    help = 'Populate services with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating service categories...')
        
        # Crear categorías de servicios
        categories = [
            {
                'name': 'Desarrollo Web',
                'description': 'Desarrollo de aplicaciones web modernas y responsivas',
                'icon': '🌐',
                'color': '#1d6ff2',
                'order': 1
            },
            {
                'name': 'Desarrollo Mobile',
                'description': 'Aplicaciones móviles nativas e híbridas',
                'icon': '📱',
                'color': '#10b981',
                'order': 2
            },
            {
                'name': 'Consultoría Tech',
                'description': 'Asesoría y consultoría tecnológica',
                'icon': '💡',
                'color': '#f59e0b',
                'order': 3
            }
        ]

        for cat_data in categories:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Crear servicios
        # Obtener tasa para conversión de ejemplo (si existe)
        try:
            from django.conf import settings as dj_settings
            usd_to_cop = getattr(dj_settings, 'USD_TO_COP_RATE', 4700)
        except Exception:
            usd_to_cop = 4700

        services = [
            {
                'title': 'Desarrollo Web Full Stack',
                'slug': 'desarrollo-web-full-stack',
                'category': ServiceCategory.objects.get(name='Desarrollo Web'),
                'description': 'Desarrollo completo de aplicaciones web con tecnologías modernas como React, Next.js, Node.js y bases de datos escalables.',
                'short_description': 'Aplicaciones web completas con frontend y backend optimizados',
                'icon': '🚀',
                'price_type': 'project',
                'price_from': float(1500.00 * usd_to_cop),
                'price_currency': 'COP',
                'duration': '3-4_weeks',
                'features': [
                    'Diseño responsivo y moderno',
                    'Frontend con React/Next.js',
                    'Backend con Node.js o Python',
                    'Base de datos optimizada',
                    'API RESTful completa',
                    'Autenticación y autorización',
                    'Panel de administración',
                    'Hosting y deploy incluido'
                ],
                'technologies': ['React', 'Next.js', 'Node.js', 'TypeScript', 'PostgreSQL'],
                'is_featured': True,
                'order': 1
            },
            {
                'title': 'Landing Page Profesional',
                'slug': 'landing-page-profesional',
                'category': ServiceCategory.objects.get(name='Desarrollo Web'),
                'description': 'Página de aterrizaje optimizada para conversiones con diseño atractivo y funcionalidades avanzadas.',
                'short_description': 'Landing pages optimizadas para conversión y SEO',
                'icon': '📄',
                'price_type': 'fixed',
                'price_from': float(500.00 * usd_to_cop),
                'price_currency': 'COP',
                'duration': '1-2_weeks',
                'features': [
                    'Diseño personalizado y responsivo',
                    'Optimización SEO',
                    'Formularios de contacto',
                    'Integración con analytics',
                    'Velocidad de carga optimizada',
                    'Hosting por 1 año incluido'
                ],
                'technologies': ['Next.js', 'TypeScript', 'Tailwind CSS'],
                'is_featured': True,
                'order': 2
            },
            {
                'title': 'App Móvil Multiplataforma',
                'slug': 'app-movil-multiplataforma',
                'category': ServiceCategory.objects.get(name='Desarrollo Mobile'),
                'description': 'Desarrollo de aplicaciones móviles para iOS y Android con un solo código base usando React Native.',
                'short_description': 'Apps móviles para iOS y Android con tecnología moderna',
                'icon': '📱',
                'price_type': 'project',
                'price_from': float(2500.00 * usd_to_cop),
                'price_currency': 'COP',
                'duration': '1-2_months',
                'features': [
                    'Una app para iOS y Android',
                    'Interfaz nativa y fluida',
                    'Integración con APIs',
                    'Notificaciones push',
                    'Publicación en stores',
                    'Soporte post-lanzamiento'
                ],
                'technologies': ['React Native', 'TypeScript', 'Firebase'],
                'is_featured': True,
                'order': 3
            },
            {
                'title': 'Consultoría Técnica',
                'slug': 'consultoria-tecnica',
                'category': ServiceCategory.objects.get(name='Consultoría Tech'),
                'description': 'Asesoría especializada en arquitectura de software, optimización de procesos y selección de tecnologías.',
                'short_description': 'Asesoría experta para optimizar tu stack tecnológico',
                'icon': '🎯',
                'price_type': 'hourly',
                'price_from': float(80.00 * usd_to_cop),
                'price_currency': 'COP',
                'duration': 'custom',
                'custom_duration': 'Flexible',
                'features': [
                    'Auditoría de código existente',
                    'Recomendaciones de arquitectura',
                    'Plan de optimización',
                    'Selección de tecnologías',
                    'Mejores prácticas de desarrollo',
                    'Documentación técnica'
                ],
                'technologies': ['Análisis de Stack', 'Arquitectura', 'Best Practices'],
                'is_featured': False,
                'order': 4
            }
        ]

        for service_data in services:
            service, created = Service.objects.get_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated services!')
        )
