#!/bin/bash

# Script de setup automático para o projeto BAH Frontend
# Uso: ./setup.sh [docker|local]

set -e

echo "🚀 BAH Frontend - Setup Automático"
echo "=================================="

# Verificar se foi passado um argumento
if [ $# -eq 0 ]; then
    echo "❓ Escolha o método de desenvolvimento:"
    echo "1) Docker (recomendado)"
    echo "2) Local"
    read -p "Digite sua escolha (1 ou 2): " choice
    
    case $choice in
        1) METHOD="docker" ;;
        2) METHOD="local" ;;
        *) echo "❌ Escolha inválida!" && exit 1 ;;
    esac
else
    METHOD=$1
fi

echo "📋 Método escolhido: $METHOD"
echo ""

# Verificar se o Git está disponível
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado. Por favor, instale o Git."
    exit 1
fi

# Setup para Docker
if [ "$METHOD" = "docker" ]; then
    echo "🐳 Configurando ambiente Docker..."
    
    # Verificar se Docker está instalado
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker não encontrado."
        echo "📋 Por favor, instale o Docker:"
        echo "   - macOS/Windows: https://www.docker.com/products/docker-desktop"
        echo "   - Linux: https://docs.docker.com/engine/install/"
        exit 1
    fi
    
    # Verificar se Docker Compose está disponível
    if ! (command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1); then
        echo "❌ Docker Compose não encontrado."
        echo "📋 Por favor, instale o Docker Compose:"
        echo "   - Versão nova: já vem integrado com Docker Desktop"
        echo "   - Versão antiga: https://docs.docker.com/compose/install/"
        exit 1
    fi
    
    echo "✅ Docker e Docker Compose encontrados!"
    echo "🔨 Construindo e iniciando containers..."
    
    # Buildar e subir os containers usando script híbrido
    ./scripts/detect-docker-compose.sh up --build -d
    
    echo ""
    echo "🎉 Setup concluído!"
    echo "📍 Aplicação rodando em: http://localhost:5173"
    echo ""
    echo "📋 Comandos úteis:"
    echo "   npm run docker:logs        # Ver logs"
    echo "   npm run docker:stop        # Parar containers"
    echo "   npm run docker:shell       # Acessar container"
    
# Setup para desenvolvimento local
elif [ "$METHOD" = "local" ]; then
    echo "💻 Configurando ambiente local..."
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js não encontrado."
        echo "📋 Por favor, instale o Node.js 24+ de:"
        echo "   https://nodejs.org/"
        exit 1
    fi
    
    # Verificar versão do Node.js
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 20 ]; then
        echo "❌ Node.js versão $NODE_VERSION encontrada."
        echo "📋 Por favor, atualize para Node.js 20+ de:"
        echo "   https://nodejs.org/"
        exit 1
    fi
    
    echo "✅ Node.js $(node -v) encontrado!"
    
    # Verificar npm
    if ! command -v npm &> /dev/null; then
        echo "❌ npm não encontrado."
        exit 1
    fi
    
    echo "✅ npm $(npm -v) encontrado!"
    echo "📦 Instalando dependências..."
    
    # Instalar dependências
    npm install
    
    echo ""
    echo "🎉 Setup concluído!"
    echo "📍 Para iniciar o desenvolvimento, execute:"
    echo "   npm run dev"
    echo ""
    echo "📋 Comandos disponíveis:"
    echo "   npm run dev        # Servidor de desenvolvimento"
    echo "   npm run build      # Build para produção"
    echo "   npm run lint       # Verificar código"
    
else
    echo "❌ Método inválido: $METHOD"
    echo "📋 Use: ./setup.sh [docker|local]"
    exit 1
fi

echo ""
echo "🔗 Documentação completa: README.md"
echo "🆘 Problemas? Verifique a seção Troubleshooting no README.md"
