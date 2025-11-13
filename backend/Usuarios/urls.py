from django.urls import path
from rest_framework import routers
from .views import UsuarioView, PrestamoView
from .authentication import (
    login_view,
    logout_view,
    refresh_token_view,
    verify_token_view,
    current_user_view,
    register_view
)

router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioView, "usuarios")
router.register(r'prestamos', PrestamoView, "prestamos")

# URLs de autenticación
auth_urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/refresh/', refresh_token_view, name='refresh_token'),
    path('auth/verify/', verify_token_view, name='verify_token'),
    path('auth/me/', current_user_view, name='current_user'),
    path('auth/register/', register_view, name='register'),
]

urlpatterns = router.urls + auth_urlpatterns

