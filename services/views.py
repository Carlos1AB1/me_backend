from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import ServiceCategory, Service
from .serializers import ServiceCategorySerializer, ServiceListSerializer, ServiceDetailSerializer

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para categorías de servicios
    """
    queryset = ServiceCategory.objects.filter(is_active=True)
    serializer_class = ServiceCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering = ['order', 'name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class ServiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para servicios
    """
    queryset = Service.objects.select_related('category').filter(is_active=True, category__is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price_type', 'duration', 'is_featured']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['title', 'order', 'created_at', 'price_from']
    ordering = ['order', '-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'by_category']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        return ServiceListSerializer

    @swagger_auto_schema(
        responses={200: ServiceListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def featured(self, request):
        """
        Obtener servicios destacados
        """
        featured_services = self.get_queryset().filter(is_featured=True)
        serializer = ServiceListSerializer(featured_services, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: ServiceListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_category(self, request):
        """
        Obtener servicios agrupados por categoría
        """
        categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('services')
        data = []
        for category in categories:
            services = category.services.filter(is_active=True)
            data.append({
                'category': ServiceCategorySerializer(category).data,
                'services': ServiceListSerializer(services, many=True).data
            })
        return Response(data)
