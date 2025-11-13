#!/bin/bash

# Script para inicializar el proyecto completo

echo "🚀 Iniciando proyecto de Gestión de Biblioteca..."
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Verificar que existe .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Archivo .env no encontrado${NC}"
    echo "Copiando .env.example a .env..."
    cp .env.example .env
    echo -e "${RED}❗ IMPORTANTE: Edita el archivo .env con credenciales seguras antes de continuar${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Archivo .env encontrado${NC}"

# 2. Detener contenedores existentes
echo ""
echo "🛑 Deteniendo contenedores existentes..."
docker-compose down -v

# 3. Construir e iniciar contenedores
echo ""
echo "🏗️  Construyendo e iniciando contenedores..."
docker-compose up --build -d

# 4. Esperar a que los servicios estén listos
echo ""
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# 5. Verificar estado de los contenedores
echo ""
echo "📊 Estado de los contenedores:"
docker-compose ps

# 6. Mostrar logs del backend
echo ""
echo "📋 Últimos logs del backend:"
docker-compose logs --tail=20 backend

# 7. Información de conexión
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 Proyecto iniciado correctamente${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📍 URLs disponibles:"
echo "   - Backend API: http://localhost:8000/api/"
echo "   - Admin Django: http://localhost:8000/admin/"
echo "   - PostgreSQL: localhost:5432"
echo ""
echo "🔑 Credenciales por defecto:"
echo "   - Superuser: superadmin / Sup3r@dm1n_S3cur3!2024"
echo "   - Admin: admin / @dm1n_S3cur3!2024"
echo ""
echo "📚 Documentación:"
echo "   - README.md"
echo "   - API_AUTHENTICATION.md"
echo "   - IMPLEMENTATION_SUMMARY.md"
echo ""
echo "🧪 Para probar el sistema de autenticación:"
echo "   python test_auth.py"
echo ""
echo "📋 Ver logs en tiempo real:"
echo "   docker-compose logs -f backend"
echo ""
echo "🛑 Detener proyecto:"
echo "   docker-compose down"
echo ""
