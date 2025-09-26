from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Usuarios'

    def ready(self):
        from django.db import connection
        from .models import Usuario, Prestamo
        from backend.utils.AVL_classes import AVLTree

        global avl_usuarios
        global avl_prestamos
        avl_usuarios=AVLTree()
        avl_prestamos=AVLTree()

        # Solo cargar datos si las tablas existen (después de migraciones)
        try:
            # Verificar si las tablas existen
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name='Usuarios_usuario'")
                if cursor.fetchone():
                    for usuario in Usuario.objects.all():
                        avl_usuarios.insert(usuario.dni,usuario)
                
                cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name='Usuarios_prestamo'")
                if cursor.fetchone():
                    for prestamo in Prestamo.objects.all():
                        avl_prestamos.insert(prestamo.id,prestamo)
        except Exception:
            # Si hay cualquier error (tabla no existe, etc.), simplemente continuar
            pass

        import Usuarios.signals
