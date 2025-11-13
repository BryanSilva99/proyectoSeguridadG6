"""
Sistema de autenticación con JWT para usuarios
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .serializers import UsuarioSerializer
from .models import Usuario


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    """
    Endpoint de login
    
    POST /api/auth/login/
    Body:
    {
        "username": "nombre_usuario",
        "password": "contraseña"
    }
    
    Retorna:
    {
        "access": "token_de_acceso",
        "refresh": "token_de_refresco",
        "user": {...datos del usuario...}
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Se requieren username y password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Autenticar usuario
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    if not user.is_active:
        return Response(
            {'error': 'Usuario inactivo'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Generar tokens JWT
    refresh = RefreshToken.for_user(user)
    
    # Serializar datos del usuario
    user_serializer = UsuarioSerializer(user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': user_serializer.data,
        'message': 'Login exitoso'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Endpoint de logout
    
    POST /api/auth/logout/
    Headers: Authorization: Bearer <access_token>
    Body:
    {
        "refresh": "refresh_token"
    }
    
    Agrega el refresh token a la blacklist para invalidarlo
    """
    try:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Se requiere el refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Blacklist el refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response(
            {'message': 'Logout exitoso'},
            status=status.HTTP_200_OK
        )
    except TokenError as e:
        return Response(
            {'error': 'Token inválido o expirado'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': 'Error al cerrar sesión'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def refresh_token_view(request):
    """
    Endpoint para refrescar el access token
    
    POST /api/auth/refresh/
    Body:
    {
        "refresh": "refresh_token"
    }
    
    Retorna:
    {
        "access": "nuevo_access_token",
        "refresh": "nuevo_refresh_token" (si ROTATE_REFRESH_TOKENS está activado)
    }
    """
    try:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Se requiere el refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken(refresh_token)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),  # Nuevo refresh token si ROTATE_REFRESH_TOKENS=True
        }, status=status.HTTP_200_OK)
        
    except TokenError as e:
        return Response(
            {'error': 'Token inválido o expirado'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token_view(request):
    """
    Endpoint para verificar si el token es válido
    
    GET /api/auth/verify/
    Headers: Authorization: Bearer <access_token>
    
    Retorna los datos del usuario si el token es válido
    """
    user_serializer = UsuarioSerializer(request.user)
    return Response({
        'valid': True,
        'user': user_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    Obtiene los datos del usuario autenticado actual
    
    GET /api/auth/me/
    Headers: Authorization: Bearer <access_token>
    """
    user_serializer = UsuarioSerializer(request.user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_view(request):
    """
    Endpoint para registrar un nuevo usuario (cliente)
    
    POST /api/auth/register/
    Body:
    {
        "username": "nombre_usuario",
        "password": "contraseña",
        "email": "email@example.com",
        "dni": "12345678",
        "full_name": "Nombre Completo",
        "address": "Dirección"
    }
    """
    serializer = UsuarioSerializer(data=request.data)
    
    if serializer.is_valid():
        # Crear usuario como cliente por defecto
        user = Usuario.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=request.data.get('password'),
            dni=serializer.validated_data['dni'],
            full_name=serializer.validated_data['full_name'],
            address=serializer.validated_data['address'],
            type='cliente'  # Por defecto es cliente
        )
        
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UsuarioSerializer(user).data,
            'message': 'Usuario registrado exitosamente'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
