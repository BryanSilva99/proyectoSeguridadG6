# Backend - Sistema de Gestión de Biblioteca

## � Descripción

Sistema backend para gestión de biblioteca con autenticación JWT, roles de usuario y gestión de préstamos de libros.

## �🔒 Configuración de Seguridad

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

## 🔐 Sistema de Autenticación JWT

El sistema implementa autenticación basada en JSON Web Tokens (JWT) con las siguientes características:

- **Access Token**: Válido por 1 hora
- **Refresh Token**: Válido por 7 días
- **Blacklist**: Los tokens se invalidan al hacer logout
- **Rotación**: Los refresh tokens se rotan automáticamente

### Endpoints de Autenticación

| Endpoint | Método | Descripción | Autenticado |
|----------|--------|-------------|-------------|
| `/api/auth/register/` | POST | Registrar nuevo usuario | No |
| `/api/auth/login/` | POST | Iniciar sesión | No |
| `/api/auth/logout/` | POST | Cerrar sesión | Sí |
| `/api/auth/refresh/` | POST | Refrescar token | No |
| `/api/auth/verify/` | GET | Verificar token | Sí |
| `/api/auth/me/` | GET | Datos del usuario actual | Sí |

Ver documentación completa en [API_AUTHENTICATION.md](API_AUTHENTICATION.md)

## 👥 Roles y Permisos

### Administrador
- ✅ Gestión completa de usuarios
- ✅ Gestión completa de libros (CRUD)
- ✅ Gestión completa de préstamos
- ✅ Acceso a estadísticas y reportes

### Cliente
- ✅ Ver catálogo de libros
- ✅ Ver y editar su perfil
- ✅ Ver sus propios préstamos
- ❌ No puede modificar libros
- ❌ No puede crear préstamos (solo administradores)

## 📡 API Endpoints

### Usuarios
- `GET /api/usuarios/` - Lista de usuarios (filtrada según rol)
- `POST /api/usuarios/` - Crear usuario (solo admin)
- `GET /api/usuarios/{dni}/` - Detalle de usuario
- `PUT /api/usuarios/{dni}/` - Actualizar usuario
- `DELETE /api/usuarios/{dni}/` - Eliminar usuario (solo admin)
- `GET /api/usuarios/me/` - Información del usuario actual
- `GET /api/usuarios/administradores/` - Lista de admins (solo admin)
- `GET /api/usuarios/clientes/` - Lista de clientes (solo admin)

### Libros
- `GET /api/libros/` - Lista de libros
- `POST /api/libros/` - Crear libro (solo admin)
- `GET /api/libros/{id}/` - Detalle de libro
- `PUT /api/libros/{id}/` - Actualizar libro (solo admin)
- `DELETE /api/libros/{id}/` - Eliminar libro (solo admin)
- `GET /api/libros/disponibles/` - Libros disponibles
- `GET /api/libros/prestados/` - Libros prestados

### Préstamos
- `GET /api/prestamos/` - Lista de préstamos (filtrada según rol)
- `POST /api/prestamos/` - Crear préstamo (solo admin)
- `GET /api/prestamos/{id}/` - Detalle de préstamo
- `PUT /api/prestamos/{id}/` - Actualizar préstamo (solo admin)
- `DELETE /api/prestamos/{id}/` - Eliminar préstamo (solo admin)
- `GET /api/prestamos/mis_prestamos/` - Préstamos del usuario actual
- `GET /api/prestamos/activos/` - Préstamos activos (solo admin)
- `GET /api/prestamos/vencidos/` - Préstamos vencidos (solo admin)
- `POST /api/prestamos/{id}/marcar_terminado/` - Marcar como terminado (solo admin)

## 🧪 Pruebas

Ejecutar el script de pruebas de autenticación:

```bash
# Asegúrate de que el servidor esté corriendo
docker-compose up

# En otra terminal, ejecuta las pruebas
python test_auth.py
```

## 📦 Dependencias Principales

- **Django 5.0.6**: Framework web
- **Django REST Framework 3.15.1**: API REST
- **djangorestframework-simplejwt 5.3.1**: Autenticación JWT
- **PostgreSQL**: Base de datos
- **django-cors-headers**: Manejo de CORS
- **python-decouple**: Gestión de variables de entorno

## � Docker

El proyecto incluye configuración completa de Docker:

- **Backend**: Django en puerto 8000
- **Base de datos**: PostgreSQL 15 en puerto 5432
- **Volúmenes**: Persistencia de datos de PostgreSQL

## �📝 Notas

- El backend estará disponible en: http://localhost:8000
- La base de datos PostgreSQL en: localhost:5432
- Las credenciales se cargan automáticamente desde el archivo `.env`
- La documentación interactiva del API está disponible en: http://localhost:8000/api/

## 🔧 Desarrollo

### Ejecutar migraciones manualmente

```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### Crear superusuario manualmente

```bash
docker-compose exec backend python manage.py createsuperuser
```

### Acceder al shell de Django

```bash
docker-compose exec backend python manage.py shell
```

### Ver logs

```bash
docker-compose logs -f backend
```

## 📖 Documentación Adicional

- [API de Autenticación](API_AUTHENTICATION.md) - Documentación completa del sistema de autenticación JWT
- [Django REST Framework](https://www.django-rest-framework.org/) - Documentación oficial
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) - Documentación de JWT
