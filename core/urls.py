from django.urls import path
from .views import (
    HealthCheckView, 
    ImageUploadView, 
    MultipleImageUploadView, 
    ImageListView, 
    ImageDeleteView
)

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('images/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('images/upload-multiple/', MultipleImageUploadView.as_view(), name='multiple-image-upload'),
    path('images/', ImageListView.as_view(), name='image-list'),
    path('images/delete/<path:file_path>/', ImageDeleteView.as_view(), name='image-delete'),
]
