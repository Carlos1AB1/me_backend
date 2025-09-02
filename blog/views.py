from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from .models import BlogPost, Category
from .serializers import BlogPostSerializer, BlogPostListSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para categorías del blog
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class BlogPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet para posts del blog
    """
    queryset = BlogPost.objects.select_related('author').prefetch_related('categories')
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_featured', 'categories']
    search_fields = ['title', 'excerpt', 'content', 'tags']
    ordering_fields = ['created_at', 'published_at', 'views_count', 'title']
    ordering = ['-published_at', '-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'recent']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer

    def get_queryset(self):
        queryset = BlogPost.objects.select_related('author').prefetch_related('categories')
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Incrementar contador de vistas al obtener un post
        """
        instance = self.get_object()
        if not request.user.is_authenticated or request.user != instance.author:
            instance.views_count += 1
            instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: BlogPostListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def featured(self, request):
        """
        Obtener posts destacados
        """
        featured_posts = self.get_queryset().filter(is_featured=True, status='published')
        serializer = BlogPostListSerializer(featured_posts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: BlogPostListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def recent(self, request):
        """
        Obtener posts recientes
        """
        recent_posts = self.get_queryset().filter(status='published')[:5]
        serializer = BlogPostListSerializer(recent_posts, many=True)
        return Response(serializer.data)
