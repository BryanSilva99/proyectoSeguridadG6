from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UsuarioSerializer, PrestamoSerializer
from .models import Usuario, Prestamo
from .permissions import IsAdministrador, IsAdministradorOrReadOnly, IsOwnerOrAdministrador


class UsuarioView(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios
    - Los administradores pueden ver y gestionar todos los usuarios
    - Los clientes solo pueden ver su propia información
    """
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar queryset según el tipo de usuario
        """
        user = self.request.user
        if user.type == 'administrador':
            # Administradores ven todos los usuarios
            return Usuario.objects.all()
        # Clientes solo ven su propio perfil
        return Usuario.objects.filter(dni=user.dni)
    
    def get_permissions(self):
        """
        Permisos según la acción
        """
        if self.action in ['create', 'destroy']:
            # Solo administradores pueden crear o eliminar usuarios
            return [IsAdministrador()]
        elif self.action in ['update', 'partial_update']:
            # Usuarios pueden actualizar su propio perfil, admins pueden actualizar cualquiera
            return [IsOwnerOrAdministrador()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Endpoint para obtener información del usuario actual
        GET /api/usuarios/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrador])
    def administradores(self, request):
        """
        Obtener lista de administradores
        GET /api/usuarios/administradores/
        """
        admins = Usuario.objects.filter(type='administrador')
        serializer = self.get_serializer(admins, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrador])
    def clientes(self, request):
        """
        Obtener lista de clientes
        GET /api/usuarios/clientes/
        """
        clientes = Usuario.objects.filter(type='cliente')
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)


class PrestamoView(viewsets.ModelViewSet):
    """
    ViewSet para gestionar préstamos
    - Los administradores pueden ver y gestionar todos los préstamos
    - Los clientes solo pueden ver sus propios préstamos
    """
    serializer_class = PrestamoSerializer
    queryset = Prestamo.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtrar préstamos según el tipo de usuario
        """
        user = self.request.user
        if user.type == 'administrador':
            # Administradores ven todos los préstamos
            return Prestamo.objects.all()
        # Clientes solo ven sus propios préstamos
        return Prestamo.objects.filter(usuario=user)
    
    def get_permissions(self):
        """
        Permisos según la acción
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Solo administradores pueden crear, actualizar o eliminar préstamos
            return [IsAdministrador()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def mis_prestamos(self, request):
        """
        Obtener préstamos del usuario actual
        GET /api/prestamos/mis_prestamos/
        """
        prestamos = Prestamo.objects.filter(usuario=request.user)
        serializer = self.get_serializer(prestamos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrador])
    def activos(self, request):
        """
        Obtener préstamos activos
        GET /api/prestamos/activos/
        """
        prestamos = Prestamo.objects.filter(status='activo')
        serializer = self.get_serializer(prestamos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrador])
    def vencidos(self, request):
        """
        Obtener préstamos vencidos
        GET /api/prestamos/vencidos/
        """
        prestamos = Prestamo.objects.filter(status='vencido')
        serializer = self.get_serializer(prestamos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdministrador])
    def marcar_terminado(self, request, pk=None):
        """
        Marcar un préstamo como terminado
        POST /api/prestamos/{id}/marcar_terminado/
        """
        prestamo = self.get_object()
        prestamo.status = 'terminado'
        prestamo.save()
        serializer = self.get_serializer(prestamo)
        return Response(serializer.data)



