from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin para mensajes de contacto
    """
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Información del contacto', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Mensaje', {
            'fields': ('subject', 'message')
        }),
        ('Estado y metadata', {
            'fields': ('status', 'ip_address', 'user_agent', 'created_at', 'updated_at')
        }),
    )
