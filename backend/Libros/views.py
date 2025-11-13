from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import LibroSerializer
from .models import Libro
from Usuarios.permissions import IsAdministradorOrReadOnly


class LibroView(viewsets.ModelViewSet):
    """
    ViewSet para gestionar libros
    - Todos los usuarios autenticados pueden ver libros (GET)
    - Solo administradores pueden crear, actualizar o eliminar libros (POST, PUT, DELETE)
    """
    serializer_class = LibroSerializer
    queryset = Libro.objects.all().order_by('-status', 'title')
    permission_classes = [IsAuthenticated, IsAdministradorOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        Obtener libros disponibles (no prestados)
        GET /api/libros/disponibles/
        """
        libros = Libro.objects.filter(status=True)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def prestados(self, request):
        """
        Obtener libros prestados
        GET /api/libros/prestados/
        """
        libros = Libro.objects.filter(status=False)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def buscar_isbn(self, request, pk=None):
        """
        Buscar libro por ISBN
        GET /api/libros/{isbn}/buscar_isbn/
        """
        try:
            libro = Libro.objects.get(isbn=pk)
            serializer = self.get_serializer(libro)
            return Response(serializer.data)
        except Libro.DoesNotExist:
            return Response(
                {'error': 'Libro no encontrado'},
                status=404
            )
