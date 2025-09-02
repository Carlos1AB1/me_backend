from django.db import models

class ContactMessage(models.Model):
    """
    Mensajes de contacto del portafolio
    """
    STATUS_CHOICES = [
        ('new', 'Nuevo'),
        ('read', 'Leído'),
        ('replied', 'Respondido'),
        ('archived', 'Archivado'),
    ]

    name = models.CharField(max_length=100, verbose_name='Nombre')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Asunto')
    message = models.TextField(verbose_name='Mensaje')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    company = models.CharField(max_length=100, blank=True, verbose_name='Empresa')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Estado')
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='Dirección IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')

    class Meta:
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
