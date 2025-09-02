from django import forms
from django.utils.html import mark_safe
from django.utils.safestring import mark_safe as safe

class ColorPickerWidget(forms.TextInput):
    """
    Widget para seleccionar colores con vista previa
    """
    
    def __init__(self, attrs=None):
        default_attrs = {'type': 'color', 'style': 'width: 100px; height: 40px;'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Renderizar el input de color
        html = super().render(name, value, attrs, renderer)
        
        # Agregar vista previa y colores predefinidos
        preview_html = f'''
        <div style="margin-top: 10px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="display: flex; flex-direction: column; align-items: center;">
                    <div id="color-preview-{name}" 
                         style="width: 60px; height: 60px; border: 2px solid #ddd; border-radius: 8px; background: {value or '#74b9ff'};">
                    </div>
                    <small style="margin-top: 5px; color: #666;">Vista previa</small>
                </div>
                <div>
                    <p style="margin: 0 0 8px 0; font-weight: bold;">Colores predefinidos:</p>
                    <div style="display: flex; gap: 5px; flex-wrap: wrap;">
        '''
        
        # Colores predefinidos para tecnologías
        predefined_colors = [
            ('#61DAFB', 'React'),
            ('#3178C6', 'TypeScript'),
            ('#F7DF1E', 'JavaScript'),
            ('#339933', 'Node.js'),
            ('#3776AB', 'Python'),
            ('#E34F26', 'HTML'),
            ('#1572B6', 'CSS'),
            ('#FF6F00', 'Firebase'),
            ('#FF9900', 'AWS'),
            ('#2496ED', 'Docker'),
            ('#F05032', 'Git'),
            ('#000000', 'Next.js'),
        ]
        
        for color, tech_name in predefined_colors:
            preview_html += f'''
                <button type="button" 
                        onclick="document.getElementById('id_{name}').value='{color}'; document.getElementById('color-preview-{name}').style.background='{color}';"
                        style="width: 25px; height: 25px; background: {color}; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; margin: 1px;"
                        title="{tech_name}">
                </button>
            '''
        
        preview_html += '''
                    </div>
                </div>
            </div>
            <script>
                document.getElementById('id_''' + name + '''').addEventListener('input', function(e) {
                    document.getElementById('color-preview-''' + name + '''').style.background = e.target.value;
                });
            </script>
        </div>
        '''
        
        html += safe(preview_html)
        return safe(html)

class ImagePreviewWidget(forms.ClearableFileInput):
    """
    Widget personalizado para mostrar vista previa de imágenes
    """
    
    def render(self, name, value, attrs=None, renderer=None):
        # Renderizar el widget original
        html = super().render(name, value, attrs, renderer)
        
        if value and hasattr(value, 'url'):
            # Agregar vista previa de la imagen
            preview_html = f'''
            <div style="margin-top: 10px;">
                <p><strong>Vista previa actual:</strong></p>
                <img src="{value.url}" 
                     style="max-width: 200px; max-height: 200px; object-fit: cover; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" 
                     alt="Vista previa" />
                <p style="font-size: 12px; color: #666; margin-top: 5px;">
                    <strong>URL:</strong> <a href="{value.url}" target="_blank">{value.url}</a>
                </p>
            </div>
            '''
            html += safe(preview_html)
        
        return safe(html)

class ImagePreviewForm(forms.ModelForm):
    """
    Formulario base que incluye vista previa de imágenes
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplicar el widget personalizado a todos los ImageField
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ImageField):
                field.widget = ImagePreviewWidget()
                field.help_text = "Formatos admitidos: JPG, PNG, GIF, WebP. Tamaño máximo: 5MB"
