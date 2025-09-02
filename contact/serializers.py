from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Serializer para mensajes de contacto
    """
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'subject', 'message', 'phone', 'company',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

class ContactFormSerializer(serializers.ModelSerializer):
    """
    Serializer para formulario de contacto público
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message', 'phone', 'company']

    def validate_email(self, value):
        """
        Validar formato de email
        """
        if not value or '@' not in value:
            raise serializers.ValidationError("Email inválido")
        return value

    def validate_message(self, value):
        """
        Validar longitud del mensaje
        """
        if len(value) < 10:
            raise serializers.ValidationError("El mensaje debe tener al menos 10 caracteres")
        return value
