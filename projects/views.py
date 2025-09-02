from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import Project
from .serializers import ProjectSerializer, ProjectListSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de proyectos
    """
    queryset = Project.objects.filter(status='published')
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'featured', 'priority']
    search_fields = ['title', 'description', 'technologies']
    ordering_fields = ['created_at', 'priority', 'title']
    ordering = ['-priority', '-created_at']

    def get_permissions(self):
        """
        Solo lectura para usuarios no autenticados
        """
        if self.action in ['list', 'retrieve', 'featured']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        return queryset

    @swagger_auto_schema(
        responses={200: ProjectListSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def featured(self, request):
        """
        Obtener proyectos destacados
        """
        featured_projects = self.get_queryset().filter(featured=True)
        serializer = ProjectListSerializer(featured_projects, many=True)
        return Response(serializer.data)
