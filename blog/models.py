from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):
    """
    Categorías para posts del blog
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descripción')
    color = models.CharField(max_length=7, default='#007bff', help_text='Color en hexadecimal', verbose_name='Color')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BlogPost(models.Model):
    """
    Posts del blog
    """
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
        ('archived', 'Archivado'),
    ]

    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    excerpt = models.TextField(max_length=300, verbose_name='Extracto')
    content = models.TextField(verbose_name='Contenido')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='Imagen destacada')
    categories = models.ManyToManyField(Category, related_name='posts', verbose_name='Categorías')
    tags = models.CharField(max_length=200, blank=True, help_text='Separar con comas', verbose_name='Etiquetas')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Estado')
    is_featured = models.BooleanField(default=False, verbose_name='Destacado')
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='Meta descripción')
    read_time = models.PositiveIntegerField(default=5, help_text='Tiempo de lectura en minutos', verbose_name='Tiempo de lectura')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Número de vistas')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Autor')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Publicado en')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        verbose_name = 'Post del Blog'
        verbose_name_plural = 'Posts del Blog'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
