from rest_framework import serializers
from .models import BlogPost, Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para categorías del blog
    """
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'color', 'posts_count']

class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializer completo para posts del blog
    """
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    categories_data = CategorySerializer(source='categories', many=True, read_only=True)
    tags_list = serializers.ReadOnlyField(source='get_tags_list')
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'categories', 'categories_data', 'tags', 'tags_list', 'status',
            'is_featured', 'meta_description', 'read_time', 'views_count',
            'author', 'author_name', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['author', 'views_count', 'created_at', 'updated_at']
    
    def get_featured_image(self, obj):
        """
        Devuelve la URL completa de la imagen
        """
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            else:
                return f"http://127.0.0.1:8000{obj.featured_image.url}"
        return None

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class BlogPostListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de posts
    """
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    categories_data = CategorySerializer(source='categories', many=True, read_only=True)
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'categories_data', 'is_featured', 'read_time', 'views_count',
            'author_name', 'published_at', 'created_at'
        ]
    
    def get_featured_image(self, obj):
        """
        Devuelve la URL completa de la imagen
        """
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            else:
                return f"http://127.0.0.1:8000{obj.featured_image.url}"
        return None
