from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SkillCategoryViewSet, SkillViewSet

router = DefaultRouter()
router.register(r'categories', SkillCategoryViewSet)
router.register(r'', SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
