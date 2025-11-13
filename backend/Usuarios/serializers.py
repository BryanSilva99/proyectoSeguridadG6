from rest_framework import serializers
from .models import Usuario, Prestamo


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Usuario
    Excluye la contraseña en las respuestas por seguridad
    """
    class Meta:
        model = Usuario
        fields = ['dni', 'username', 'email', 'full_name', 'address', 'type', 
                  'is_active', 'is_staff', 'date_joined', 'last_login']
        read_only_fields = ['date_joined', 'last_login']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear usuarios (incluye password)
    """
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Usuario
        fields = ['dni', 'username', 'email', 'password', 'password_confirm',
                  'full_name', 'address', 'type']
    
    def validate(self, data):
        """
        Validar que las contraseñas coincidan
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden"
            })
        return data
    
    def create(self, validated_data):
        """
        Crear usuario con contraseña hasheada
        """
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(password=password, **validated_data)
        return user


class PrestamoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Prestamo
    Incluye información detallada del usuario y libro
    """
    usuario_detail = UsuarioSerializer(source='usuario', read_only=True)
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    
    class Meta:
        model = Prestamo
        fields = '__all__'
        read_only_fields = ['id', 'start_date', 'end_date']
