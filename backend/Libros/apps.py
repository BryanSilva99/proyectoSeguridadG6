from django.apps import AppConfig


class LibrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Libros'
    
    def ready(self):
        from django.db import connection
        from .models import Libro
        from backend.utils.AVL_classes import AVLTree

        global avl_libros
        avl_libros=AVLTree()

        # Solo cargar datos si la tabla existe (después de migraciones)
        try:
            # Verificar si la tabla existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name='Libros_libro'")
                if cursor.fetchone():
                    for libro in Libro.objects.all():
                        avl_libros.insert(libro.isbn,libro)
        except Exception:
            # Si hay cualquier error (tabla no existe, etc.), simplemente continuar
            pass

        import Libros.signals
