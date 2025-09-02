from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from decimal import Decimal, InvalidOperation
import re

from .models import ServiceCategory, Service, ServiceFeature


def _clean_number_string(value: str) -> Decimal:
    """Convierte una cadena con separadores comunes a Decimal.

    Soporta formatos como:
    - "1,234.56" (coma miles, punto decimal)
    - "1.234,56" (punto miles, coma decimal)
    - "649,000" (coma como separador de miles)
    - "649000" (sin separadores)
    También elimina símbolos de moneda y espacios.
    """
    if value is None:
        raise InvalidOperation("None value")

    s = str(value).strip()

    # Eliminar el símbolo de moneda y espacios
    s = re.sub(r"[^0-9,\.\-]", "", s)

    # Si tiene coma y no punto
    if s.count(',') > 0 and s.count('.') == 0:
        parts = s.split(',')
        # Si la parte decimal parece tener 3 dígitos, asumimos coma como separador de miles
        if len(parts[-1]) == 3:
            s = s.replace(',', '')
        else:
            s = s.replace(',', '.')
    # Si tiene punto y no coma
    elif s.count('.') > 0 and s.count(',') == 0:
        parts = s.split('.')
        if len(parts[-1]) == 3:
            s = s.replace('.', '')
        # en otro caso dejamos el punto como separador decimal
    # Si tiene ambos, determinamos cuál es decimal por la última aparición
    elif s.count('.') > 0 and s.count(',') > 0:
        if s.rfind(',') > s.rfind('.'):
            # coma aparece después => coma decimal, puntos miles
            s = s.replace('.', '').replace(',', '.')
        else:
            # punto aparece después => punto decimal, quitar comas
            s = s.replace(',', '')

    # Finalmente, si queda vacío
    if s == '' or s == '-' or s == '.':
        raise InvalidOperation(f"No numeric content in '{value}'")

    return Decimal(s)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')
    prepopulated_fields = {}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price_type', 'price_offer_display', 'price_display', 'duration', 'is_featured', 'image_preview', 'is_active', 'order')
    list_filter = ('category', 'price_type', 'duration', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', '-created_at')
    readonly_fields = ['image_preview']
    
    class ServiceAdminForm(forms.ModelForm):
        """Form del admin que acepta entradas con separadores y las convierte a Decimal."""
        # Usar texto para permitir separadores de miles y decimales locales
        price_from = forms.CharField(required=False, label='Precio desde')
        price_offer = forms.CharField(required=False, label='Precio de oferta')

        class Meta:
            model = Service
            fields = '__all__'

        def clean_price_from(self):
            raw = self.cleaned_data.get('price_from')
            if raw in (None, ''):
                return None
            try:
                dec = _clean_number_string(raw)
            except Exception:
                raise forms.ValidationError(f"Valor de precio inválido: {raw}")
            return dec.quantize(Decimal('0.01'))

        def clean_price_offer(self):
            raw = self.cleaned_data.get('price_offer')
            if raw in (None, ''):
                return None
            try:
                dec = _clean_number_string(raw)
            except Exception:
                raise forms.ValidationError(f"Valor de precio inválido: {raw}")
            return dec.quantize(Decimal('0.01'))

    form = ServiceAdminForm
    
    def image_preview(self, obj):
        """
        Muestra una vista previa de la imagen en el admin
        """
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "Sin imagen"
    image_preview.short_description = "Vista previa"

    def price_display(self, obj):
        return obj.get_price_display()
    price_display.short_description = 'Precio'

    def price_offer_display(self, obj):
        return obj.get_offer_display() if obj and obj.get_offer_display() else ''
    price_offer_display.short_description = 'Oferta'
    
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'slug', 'category', 'description', 'short_description', 'icon', 'image', 'image_preview')
        }),
        ('Precio', {
            'fields': ('price_type', 'price_from', 'price_offer', 'price_currency', 'show_price')
        }),
        ('Duración', {
            'fields': ('duration', 'custom_duration')
        }),
        ('Características y Tecnologías', {
            'fields': ('features', 'technologies'),
            'classes': ('collapse',)
        }),
        ('Configuración', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        })
    )

@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'service', 'is_included', 'additional_cost', 'order')
    list_filter = ('is_included', 'service__category')
    search_fields = ('title', 'description', 'service__title')
    ordering = ('service', 'order', 'title')

    class ServiceFeatureAdminForm(forms.ModelForm):
        additional_cost = forms.CharField(required=False, label='Costo adicional')

        class Meta:
            model = ServiceFeature
            fields = '__all__'

        def clean_additional_cost(self):
            raw = self.cleaned_data.get('additional_cost')
            if raw in (None, ''):
                return None
            try:
                dec = _clean_number_string(raw)
            except Exception:
                raise forms.ValidationError(f"Valor inválido: {raw}")
            return dec.quantize(Decimal('0.01'))

    form = ServiceFeatureAdminForm
