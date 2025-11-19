#!/bin/bash
set -e

echo "🚀 Iniciando deploy em produção"
echo "Commit: $CI_COMMIT_SHORT_SHA"
echo "Branch: $CI_COMMIT_REF_NAME"

# Criar .env.prod
echo "📝 Criando .env.prod..."
cat > .env.prod << EOF
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
JWT_SECRET=${JWT_SECRET}
JWT_TTL=${JWT_TTL}
JWT_ISS=${JWT_ISS}
CORS_ORIGINS=${CORS_ORIGINS}
UMAMI_DATABASE=${UMAMI_DATABASE}
UMAMI_APP_SECRET=${UMAMI_APP_SECRET}
UMAMI_DATABASE_NAME=${UMAMI_DATABASE_NAME}
UMAMI_DATABASE_USER=${UMAMI_DATABASE_USER}
UMAMI_DATABASE_PASSWORD=${UMAMI_DATABASE_PASSWORD}
ENVIRONMENT=production
EOF

echo "📦 Parando containers antigos..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod down || true

echo "🧹 Limpando recursos..."
docker system prune -af --filter "until=24h" || true

echo "🔨 Building images..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod build --no-cache

echo "🚢 Subindo containers..."
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

echo "⏳ Aguardando 30s..."
sleep 30

echo "🔍 Status dos containers:"
docker-compose -f docker-compose.prod.yml ps

echo "📋 Logs da aplicação:"
docker-compose -f docker-compose.prod.yml logs --tail=50 app

echo "🔥 Limpando .env.prod"
rm -f .env.prod

echo "✨ Deploy concluído com sucesso!"
echo "🌐 URL: http://${EC2_PUBLIC_DNS}:8000/docs"
