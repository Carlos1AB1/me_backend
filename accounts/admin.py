from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin personalizado para CustomUser
    """
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_active', 'is_verified', 'date_joined']
    list_filter = ['is_active', 'is_verified', 'is_staff', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': (
                'bio', 'avatar', 'birth_date', 'phone', 
                'linkedin_url', 'github_url', 'website_url', 
                'location', 'is_verified'
            )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': (
                'email', 'first_name', 'last_name', 'bio'
            )
        }),
    )
