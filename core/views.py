from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import os
import uuid
from PIL import Image
import io


class HealthCheckView(APIView):
    """
    Vista para verificar el estado de la API
    """
    
    @swagger_auto_schema(
        responses={200: openapi.Response('API funcionando correctamente')}
    )
    def get(self, request):
        return Response({
            'status': 'ok',
            'message': 'API funcionando correctamente',
            'version': '1.0.0'
        }, status=status.HTTP_200_OK)


class ImageUploadView(APIView):
    """
    Vista para subir una imagen individual
    """
    parser_classes = (MultiPartParser, FormParser)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('category', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        ],
        responses={201: openapi.Response('Imagen subida exitosamente')}
    )
    def post(self, request):
        try:
            if 'image' not in request.FILES:
                return Response(
                    {'error': 'No se proporcionó ninguna imagen'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            image_file = request.FILES['image']
            category = request.data.get('category', 'general')
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image_file.content_type not in allowed_types:
                return Response(
                    {'error': f'Tipo de archivo no válido. Solo se permiten: {", ".join(allowed_types)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar tamaño (5MB máximo)
            max_size = 5 * 1024 * 1024  # 5MB
            if image_file.size > max_size:
                return Response(
                    {'error': 'El archivo es muy grande. Máximo permitido: 5MB'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generar nombre único para el archivo
            file_extension = os.path.splitext(image_file.name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Crear directorio de categoria si no existe
            upload_path = os.path.join(category, unique_filename)
            
            # Optimizar imagen (opcional)
            image = Image.open(image_file)
            
            # Convertir a RGB si es necesario
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            
            # Redimensionar si es muy grande (máximo 1920x1080)
            max_width, max_height = 1920, 1080
            if image.width > max_width or image.height > max_height:
                image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Guardar imagen optimizada
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Guardar archivo
            file_path = default_storage.save(upload_path, ContentFile(output.read()))
            
            # Construir URL completa
            if hasattr(settings, 'MEDIA_URL'):
                file_url = f"{settings.MEDIA_URL}{file_path}"
            else:
                file_url = f"/media/{file_path}"
            
            return Response({
                'message': 'Imagen subida exitosamente',
                'file_path': file_path,
                'file_url': file_url,
                'category': category,
                'original_name': image_file.name
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error al subir la imagen: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MultipleImageUploadView(APIView):
    """
    Vista para subir múltiples imágenes
    """
    parser_classes = (MultiPartParser, FormParser)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('images', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
            openapi.Parameter('category', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
        ],
        responses={201: openapi.Response('Imágenes subidas exitosamente')}
    )
    def post(self, request):
        try:
            if 'images' not in request.FILES:
                return Response(
                    {'error': 'No se proporcionaron imágenes'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            images = request.FILES.getlist('images')
            category = request.data.get('category', 'general')
            
            if len(images) > 10:  # Límite de 10 imágenes por vez
                return Response(
                    {'error': 'Máximo 10 imágenes por vez'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            uploaded_files = []
            errors = []
            
            for image_file in images:
                try:
                    # Validar tipo de archivo
                    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
                    if image_file.content_type not in allowed_types:
                        errors.append(f'{image_file.name}: Tipo de archivo no válido')
                        continue
                    
                    # Validar tamaño
                    max_size = 5 * 1024 * 1024  # 5MB
                    if image_file.size > max_size:
                        errors.append(f'{image_file.name}: Archivo muy grande (máximo 5MB)')
                        continue
                    
                    # Procesar imagen igual que en upload individual
                    file_extension = os.path.splitext(image_file.name)[1]
                    unique_filename = f"{uuid.uuid4()}{file_extension}"
                    upload_path = os.path.join(category, unique_filename)
                    
                    image = Image.open(image_file)
                    if image.mode in ('RGBA', 'P'):
                        image = image.convert('RGB')
                    
                    max_width, max_height = 1920, 1080
                    if image.width > max_width or image.height > max_height:
                        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    output = io.BytesIO()
                    image.save(output, format='JPEG', quality=85, optimize=True)
                    output.seek(0)
                    
                    file_path = default_storage.save(upload_path, ContentFile(output.read()))
                    
                    if hasattr(settings, 'MEDIA_URL'):
                        file_url = f"{settings.MEDIA_URL}{file_path}"
                    else:
                        file_url = f"/media/{file_path}"
                    
                    uploaded_files.append({
                        'file_path': file_path,
                        'file_url': file_url,
                        'original_name': image_file.name
                    })
                    
                except Exception as e:
                    errors.append(f'{image_file.name}: {str(e)}')
            
            response_data = {
                'message': f'Procesadas {len(uploaded_files)} imágenes exitosamente',
                'uploaded_files': uploaded_files,
                'category': category
            }
            
            if errors:
                response_data['errors'] = errors
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Error al subir las imágenes: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImageListView(APIView):
    """
    Vista para listar imágenes por categoría
    """
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
        responses={200: openapi.Response('Lista de imágenes')}
    )
    def get(self, request):
        try:
            category = request.query_params.get('category', None)
            
            # Obtener todas las imágenes del directorio media
            media_root = settings.MEDIA_ROOT
            images = []
            
            if category:
                category_path = os.path.join(media_root, category)
                if os.path.exists(category_path):
                    for filename in os.listdir(category_path):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                            file_path = os.path.join(category, filename)
                            file_url = f"{settings.MEDIA_URL}{file_path}"
                            images.append({
                                'file_path': file_path,
                                'file_url': file_url,
                                'filename': filename,
                                'category': category
                            })
            else:
                # Listar todas las imágenes de todas las categorías
                for root, dirs, files in os.walk(media_root):
                    for filename in files:
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                            full_path = os.path.join(root, filename)
                            rel_path = os.path.relpath(full_path, media_root)
                            file_url = f"{settings.MEDIA_URL}{rel_path}"
                            category_name = os.path.dirname(rel_path) if os.path.dirname(rel_path) else 'general'
                            images.append({
                                'file_path': rel_path,
                                'file_url': file_url,
                                'filename': filename,
                                'category': category_name
                            })
            
            return Response({
                'images': images,
                'count': len(images),
                'category': category
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al listar las imágenes: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ImageDeleteView(APIView):
    """
    Vista para eliminar una imagen
    """
    
    @swagger_auto_schema(
        responses={200: openapi.Response('Imagen eliminada exitosamente')}
    )
    def delete(self, request, file_path):
        try:
            # Decodificar el path (en caso de que tenga caracteres especiales)
            import urllib.parse
            file_path = urllib.parse.unquote(file_path)
            
            # Verificar que el archivo existe
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                return Response({
                    'message': 'Imagen eliminada exitosamente',
                    'file_path': file_path
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Imagen no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            return Response(
                {'error': f'Error al eliminar la imagen: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
