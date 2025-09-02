from django.urls import path
from .views import ContactMessageView, ContactFormView

urlpatterns = [
    path('messages/', ContactMessageView.as_view(), name='contact-messages'),
    path('send/', ContactFormView.as_view(), name='contact-send'),
]
