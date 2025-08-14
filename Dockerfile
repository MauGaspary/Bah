# Dockerfile para desenvolvimento
FROM node:24-alpine

# Instalar dependências do sistema
RUN apk add --no-cache git

# Definir diretório de trabalho
WORKDIR /app

# Copiar package files primeiro (para cache das dependências)
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar o resto do código
COPY . .

# Expor porta do Vite
EXPOSE 5173

# Comando para desenvolvimento (com hot reload)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
