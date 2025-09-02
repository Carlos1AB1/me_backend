from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogPostViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'', BlogPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
