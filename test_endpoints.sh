#!/bin/bash

# Script para testar os endpoints da API

echo "Testando endpoints da API BAH"
echo "================================="

BASE_URL="http://localhost:8000"

echo ""
echo "1. Listando todos os admins (dados do seed):"
curl -s "$BASE_URL/admin/" | python3 -m json.tool

echo ""
echo "2. Criando novo admin:"
curl -s -X POST "$BASE_URL/admin/" \
  -H "Content-Type: application/json" \
  -d '{"username": "teste.usuario", "email": "teste@bah.com.br"}' | python3 -m json.tool

echo ""
echo "3. Listando todos os admins novamente:"
curl -s "$BASE_URL/admin/" | python3 -m json.tool

echo ""
echo "4. Buscando admin por ID (1):"
curl -s "$BASE_URL/admin/id/1" | python3 -m json.tool

echo ""
echo "5. Buscando admin por email:"
curl -s "$BASE_URL/admin/email/admin@bah.com.br" | python3 -m json.tool

echo ""
echo "Testes concluídos"
