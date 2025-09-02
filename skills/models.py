from django.db import models

class SkillCategory(models.Model):
    """
    Categorías de habilidades
    """
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    icon = models.CharField(max_length=50, blank=True, help_text='Clase CSS o emoji', verbose_name='Icono')
    order = models.PositiveIntegerField(default=0, verbose_name='Orden')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría de Habilidad'
        verbose_name_plural = 'Categorías de Habilidades'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Skill(models.Model):
    """
    Habilidades técnicas
    """
    LEVEL_CHOICES = [
        ('Básico', 'Básico'),
        ('Intermedio', 'Intermedio'),
        ('Experto', 'Experto'),
    ]

    name = models.CharField(max_length=100, verbose_name='Nombre')
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills', verbose_name='Categoría')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='Nivel')
    icon = models.CharField(max_length=50, blank=True, help_text='Emoji o clase CSS', verbose_name='Icono')
    image = models.ImageField(upload_to='skills/', blank=True, null=True, verbose_name='Imagen')
    sub_icon = models.CharField(max_length=50, blank=True, help_text='Emoji o clase CSS para tecnología relacionada (ej: Spring para Java)', verbose_name='Sub-Icono')
    sub_image = models.ImageField(upload_to='skills/sub/', blank=True, null=True, verbose_name='Sub-Imagen')
    color = models.CharField(
        max_length=7, 
        default='#74b9ff', 
        help_text='Color hexadecimal para el fondo del ícono (ej: #74b9ff)', 
        verbose_name='Color'
    )
    gradient_type = models.CharField(
        max_length=20,
        choices=[
            ('linear-left', 'Degradado Horizontal (Izq → Der)'),
            ('linear-right', 'Degradado Horizontal (Der → Izq)'),
            ('linear-top', 'Degradado Vertical (Arriba → Abajo)'),
            ('linear-bottom', 'Degradado Vertical (Abajo → Arriba)'),
            ('linear-diagonal-1', 'Degradado Diagonal (↘)'),
            ('linear-diagonal-2', 'Degradado Diagonal (↙)'),
            ('linear-diagonal-3', 'Degradado Diagonal (↗)'),
            ('linear-diagonal-4', 'Degradado Diagonal (↖)'),
            ('radial-center', 'Degradado Radial (Centro)'),
            ('radial-corner', 'Degradado Radial (Esquina)'),
            ('conic', 'Degradado Cónico'),
            ('solid', 'Color Sólido'),
        ],
        default='linear-diagonal-1',
        verbose_name='Tipo de Degradado'
    )
    gradient_css = models.TextField(
        blank=True,
        verbose_name='CSS del Degradado Personalizado',
        help_text='Ejemplo: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%). Si está vacío, se usará el color y tipo seleccionados arriba.'
    )
    background_type = models.CharField(
        max_length=20,
        choices=[
            ('transparent', 'Sin Fondo (Transparente)'),
            ('solid', 'Color Sólido'),
            ('gradient', 'Degradado'),
        ],
        default='gradient',
        verbose_name='Tipo de Fondo'
    )
    description = models.TextField(blank=True, verbose_name='Descripción')
    years_experience = models.PositiveIntegerField(default=0, verbose_name='Años de experiencia')
    is_featured = models.BooleanField(default=False, verbose_name='Destacada')
    order = models.PositiveIntegerField(default=0, verbose_name='Orden')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'
        ordering = ['order', '-created_at', 'category', 'name']  # Orden manual primero, luego fecha
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.category.name})"
