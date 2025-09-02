from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import SkillCategory, Skill
from .serializers import SkillCategorySerializer, SkillSerializer, SkillCategoryListSerializer

class SkillCategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para categorías de habilidades
    """
    queryset = SkillCategory.objects.filter(is_active=True)
    serializer_class = SkillCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering = ['order', 'name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return SkillCategoryListSerializer
        return SkillCategorySerializer

class SkillViewSet(viewsets.ModelViewSet):
    """
    ViewSet para habilidades
    """
    queryset = Skill.objects.select_related('category').filter(category__is_active=True)
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'level', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'order', 'years_experience']
    ordering = ['category__order', 'order', 'name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured', 'by_category']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        responses={200: SkillSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def featured(self, request):
        """
        Obtener habilidades destacadas
        """
        featured_skills = self.get_queryset().filter(is_featured=True)
        serializer = SkillSerializer(featured_skills, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={200: SkillSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_category(self, request):
        """
        Obtener habilidades agrupadas por categoría
        """
        categories = SkillCategory.objects.filter(is_active=True).prefetch_related('skills')
        data = []
        for category in categories:
            skills = category.skills.all()
            data.append({
                'category': SkillCategoryListSerializer(category).data,
                'skills': SkillSerializer(skills, many=True).data
            })
        return Response(data)
