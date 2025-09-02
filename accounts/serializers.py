from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de usuarios
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'username', 'first_name', 'last_name', 
            'password', 'password_confirm', 'bio', 'phone',
            'linkedin_url', 'github_url', 'website_url', 'location'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuarios
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales inválidas')
            if not user.is_active:
                raise serializers.ValidationError('Cuenta desactivada')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email y contraseña son requeridos')

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para perfil de usuario
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'bio', 'avatar', 'birth_date', 'phone', 'linkedin_url', 'github_url',
            'website_url', 'location', 'is_verified', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'email', 'is_verified', 'date_joined', 'last_login']

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar perfil de usuario
    """
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'bio', 'avatar', 'birth_date', 
            'phone', 'linkedin_url', 'github_url', 'website_url', 'location'
        ]

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para cambio de contraseña
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Las nuevas contraseñas no coinciden")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Contraseña actual incorrecta")
        return value
