from rest_framework import serializers
from .models import Project


from .models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'order']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            # Devuelve la URL absoluta por defecto
            return f"http://127.0.0.1:8000{obj.image.url}"
        return None

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer para proyectos
    """
    technologies_list = serializers.ReadOnlyField(source='get_technologies_list')
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'images', 'github_url', 'live_url', 'technologies', 'technologies_list',
            'priority', 'status', 'featured', 'start_date', 'end_date',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']



    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ProjectListSerializer(serializers.ModelSerializer):
    technologies_list = serializers.ReadOnlyField(source='get_technologies_list')
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'images',
            'technologies_list', 'priority', 'featured', 'github_url', 'live_url'
        ]
