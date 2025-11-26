from rest_framework import serializers
from .models import ServiceCategory, Service, ServiceFeature

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'icon', 'color', 'order']

class ServiceFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFeature
        fields = ['id', 'title', 'description', 'icon', 'is_included', 'additional_cost', 'order']

class ServiceListSerializer(serializers.ModelSerializer):
    """
    Serializer para lista de servicios (información básica)
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    price_display = serializers.SerializerMethodField()
    price_offer_display = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'slug', 'category', 'category_name', 'category_icon',
            'short_description', 'icon', 'image', 'price_type', 'price_display',
            'price_offer_display',
            'duration', 'duration_display', 'is_featured', 'order'
        ]

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_price_display(self, obj):
        return obj.get_price_display()

    def get_price_offer_display(self, obj):
        return obj.get_offer_display()

    def get_duration_display(self, obj):
        return obj.get_duration_display()

class ServiceDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para detalle completo de servicios
    """
    category = ServiceCategorySerializer(read_only=True)
    additional_features = ServiceFeatureSerializer(many=True, read_only=True)
    price_display = serializers.SerializerMethodField()
    price_offer_display = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id', 'title', 'slug', 'category', 'description', 'short_description',
            'icon', 'image', 'price_type', 'price_from', 'price_currency',
            'price_offer', 'price_offer_display',
            'price_display', 'duration', 'custom_duration', 'duration_display',
            'features', 'technologies', 'additional_features', 'is_featured',
            'show_price', 'order', 'meta_description', 'meta_keywords',
            'created_at', 'updated_at'
        ]

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_price_display(self, obj):
        return obj.get_price_display()

    def get_price_offer_display(self, obj):
        return obj.get_offer_display()

    def get_duration_display(self, obj):
        return obj.get_duration_display()
