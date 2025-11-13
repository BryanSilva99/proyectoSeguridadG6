"""
Permisos personalizados para el sistema
"""
from rest_framework import permissions


class IsAdministrador(permissions.BasePermission):
    """
    Permiso personalizado que solo permite acceso a administradores
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.type == 'administrador'
        )


class IsAdministradorOrReadOnly(permissions.BasePermission):
    """
    Permiso que permite lectura a todos los autenticados,
    pero escritura solo a administradores
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.type == 'administrador'
        )


class IsOwnerOrAdministrador(permissions.BasePermission):
    """
    Permiso que permite acceso al dueño del objeto o a administradores
    """
    def has_object_permission(self, request, view, obj):
        # Administradores tienen acceso total
        if request.user.type == 'administrador':
            return True
        
        # Los usuarios solo pueden acceder a sus propios objetos
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        
        return obj == request.user
