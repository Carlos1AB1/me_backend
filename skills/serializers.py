from rest_framework import serializers
from .models import SkillCategory, Skill

class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer para habilidades
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()
    sub_image = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'category', 'category_name', 'level', 'icon', 'image', 'sub_icon', 'sub_image', 'color', 'gradient_type', 'gradient_css', 'background_type',
            'description', 'years_experience', 'is_featured', 'order'
        ]
    
    def get_image(self, obj):
        """
        Devuelve la URL completa de la imagen
        """
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            else:
                # Fallback para cuando no hay request en el contexto
                return f"http://127.0.0.1:8000{obj.image.url}"
        return None
    
    def get_sub_image(self, obj):
        """
        Devuelve la URL completa de la sub-imagen
        """
        if obj.sub_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.sub_image.url)
            else:
                # Fallback para cuando no hay request en el contexto
                return f"http://127.0.0.1:8000{obj.sub_image.url}"
        return None

class SkillCategorySerializer(serializers.ModelSerializer):
    """
    Serializer para categorías de habilidades
    """
    skills = SkillSerializer(many=True, read_only=True)
    skills_count = serializers.IntegerField(source='skills.count', read_only=True)

    class Meta:
        model = SkillCategory
        fields = [
            'id', 'name', 'description', 'icon', 'order', 'is_active',
            'skills', 'skills_count'
        ]

class SkillCategoryListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de categorías
    """
    skills_count = serializers.IntegerField(source='skills.count', read_only=True)

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'description', 'icon', 'order', 'skills_count']
