from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.safestring import mark_safe
from django import forms
from core.widgets import ImagePreviewWidget, ColorPickerWidget
from .models import SkillCategory, Skill

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    """
    Admin para categorías de habilidades
    """
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Admin para habilidades
    """
    list_display = ['name', 'category', 'level', 'years_experience', 'is_featured', 'image_preview', 'order']
    list_filter = ['category', 'level', 'is_featured']
    search_fields = ['name', 'description']
    list_editable = ['level', 'is_featured', 'order']
    ordering = ['category', 'order', 'name']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """
        Muestra una vista previa de la imagen en el admin
        """
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "Sin imagen"
    image_preview.short_description = "Vista previa"
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Personalizar el widget para campos específicos
        """
        if db_field.name == 'image':
            kwargs['widget'] = ImagePreviewWidget
        elif db_field.name == 'sub_image':
            kwargs['widget'] = ImagePreviewWidget
        elif db_field.name == 'color':
            kwargs['widget'] = ColorPickerWidget
        elif db_field.name == 'gradient_css':
            kwargs['widget'] = forms.Textarea(attrs={
                'rows': 3, 
                'cols': 60,
                'placeholder': 'Ejemplo: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%)'
            })
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    fieldsets = (
        ('Información básica', {
            'fields': ('name', 'category', 'level', 'description')
        }),
        ('Visualización', {
            'fields': ('icon', 'image', 'image_preview', 'sub_icon', 'sub_image', 'background_type', 'color', 'gradient_type', 'gradient_css')
        }),
        ('Configuración', {
            'fields': ('years_experience', 'is_featured', 'order')
        }),
    )
