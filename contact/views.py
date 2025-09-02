from rest_framework import status, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ContactMessage
from .serializers import ContactMessageSerializer, ContactFormSerializer

class ContactMessageView(ListAPIView):
    """
    Vista para listar mensajes de contacto (solo para admin)
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering = ['-created_at']

class ContactFormView(APIView):
    """
    Vista para enviar mensajes de contacto
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=ContactFormSerializer,
        responses={
            201: openapi.Response('Mensaje enviado exitosamente'),
            400: 'Error de validación'
        }
    )
    def post(self, request):
        """
        Enviar mensaje de contacto
        """
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener información adicional de la request
            contact_message = serializer.save()
            
            # Obtener IP y User Agent
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            contact_message.ip_address = ip
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact_message.save()

            return Response({
                'message': 'Mensaje enviado exitosamente. Te contactaré pronto.',
                'id': contact_message.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
