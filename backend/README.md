# Backend - Sistema de Gestión de Biblioteca

## 🔒 Configuración de Seguridad

### Variables de Entorno

Este proyecto utiliza variables de entorno para proteger información sensible. **NUNCA** subas el archivo `.env` al repositorio.

#### Configuración Inicial

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```

2. Edita el archivo `.env` y configura tus credenciales seguras:
   - `DB_PASSWORD`: Contraseña de la base de datos (mínimo 16 caracteres, incluye símbolos)
   - `SECRET_KEY`: Clave secreta de Django (genera una nueva con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `SUPERUSER_PASSWORD`: Contraseña del superusuario (mínimo 12 caracteres, incluye mayúsculas, minúsculas, números y símbolos)
   - `ADMIN_PASSWORD`: Contraseña del administrador (mínimo 12 caracteres, incluye mayúsculas, minúsculas, números y símbolos)

3. **IMPORTANTE**: Asegúrate de que el archivo `.env` esté en `.gitignore`

### Buenas Prácticas de Seguridad

- ✅ Usa contraseñas fuertes y únicas
- ✅ Nunca compartas tus credenciales
- ✅ Rota las credenciales periódicamente
- ✅ En producción, cambia `DEBUG=False`
- ✅ Usa HTTPS en producción
- ❌ Nunca hagas commit del archivo `.env`
- ❌ No uses contraseñas por defecto en producción

## 🚀 Iniciar el Proyecto

```bash
# Construir e iniciar los contenedores
docker-compose up --build

# Detener los contenedores
docker-compose down

# Detener y eliminar volúmenes (limpieza completa)
docker-compose down -v
```

## 📝 Notas

- El backend estará disponible en: http://localhost:8000
- La base de datos PostgreSQL en: localhost:5432
- Las credenciales se cargan automáticamente desde el archivo `.env`
