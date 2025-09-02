from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, BlogPost

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin para categorías del blog
    """
    list_display = ['name', 'slug', 'color', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin para posts del blog
    """
    list_display = ['title', 'status', 'is_featured', 'image_preview', 'author', 'views_count', 'created_at']
    list_filter = ['status', 'is_featured', 'categories', 'created_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    filter_horizontal = ['categories']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        """
        Muestra una vista previa de la imagen en el admin
        """
        if obj.featured_image:
            return mark_safe(f'<img src="{obj.featured_image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "Sin imagen"
    image_preview.short_description = "Vista previa"
    
    fieldsets = (
        ('Contenido', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image', 'image_preview')
        }),
        ('Categorización', {
            'fields': ('categories', 'tags')
        }),
        ('SEO', {
            'fields': ('meta_description', 'read_time')
        }),
        ('Configuración', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.author = request.user
        super().save_model(request, obj, form, change)
