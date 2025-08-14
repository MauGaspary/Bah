#!/bin/bash

# Script híbrido para detectar e executar docker-compose ou docker compose
# Uso: ./scripts/detect-docker-compose.sh [comando]

if command -v docker-compose &> /dev/null; then
    docker-compose "$@"
elif docker compose version &> /dev/null 2>&1; then
    docker compose "$@"
else
    echo "ERROR: Neither docker-compose nor docker compose found" >&2
    exit 1
fi
