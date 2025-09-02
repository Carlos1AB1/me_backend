from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserUpdateSerializer, ChangePasswordSerializer
)

class UserRegistrationView(APIView):
    """
    Vista para registro de usuarios
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response('Usuario creado exitosamente'),
            400: 'Error de validación'
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    Vista para login de usuarios
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response('Login exitoso'),
            401: 'Credenciales inválidas'
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login exitoso',
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(RetrieveUpdateAPIView):
    """
    Vista para obtener y actualizar perfil de usuario
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserProfileSerializer

    @swagger_auto_schema(
        responses={200: UserProfileSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserProfileSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        responses={200: UserProfileSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class ChangePasswordView(APIView):
    """
    Vista para cambiar contraseña
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response('Contraseña cambiada exitosamente'),
            400: 'Error de validación'
        }
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                'message': 'Contraseña cambiada exitosamente'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    responses={200: openapi.Response('Logout exitoso')}
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Vista para logout (invalidar token)
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Error al hacer logout'
        }, status=status.HTTP_400_BAD_REQUEST)
