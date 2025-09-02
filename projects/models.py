from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    Modelo para proyectos del portafolio
    """
    PRIORITY_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('archived', 'Archivado'),
    ]

    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Descripción')
    short_description = models.CharField(max_length=300, verbose_name='Descripción corta')
    # El campo image se elimina, ahora se usará ProjectImage
    github_url = models.URLField(blank=True, verbose_name='URL de GitHub')
    live_url = models.URLField(blank=True, verbose_name='URL del sitio en vivo')
    technologies = models.CharField(max_length=500, help_text='Separar con comas', verbose_name='Tecnologías')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name='Prioridad')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Estado')
    featured = models.BooleanField(default=False, verbose_name='Destacado')
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(blank=True, null=True, verbose_name='Fecha de finalización')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Creado por')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title

    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]

# Nuevo modelo para imágenes múltiples por proyecto
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')
    order = models.PositiveIntegerField(default=0, help_text='Orden de la imagen en la galería')

    class Meta:
        ordering = ['order']
        verbose_name = 'Imagen de proyecto'
        verbose_name_plural = 'Imágenes de proyecto'

    def __str__(self):
        return f"Imagen de {self.project.title} (orden {self.order})"
