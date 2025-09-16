# Bah – Plataforma de Inovação de Caxias do Sul

## Desenvolvimento Local

### Instalar pipenv

```Bash
pip install pipenv
```

### Instalar dependências do projeto

```Bash
pipenv install --dev
```

### Ativar virtual environment

```Bash
pipenv shell
```

**Nota para Windows**: Se encontrar erro relacionado ao `pypiwin32`, execute:

```Shell
pip install pypiwin32

# Ou se for pywin32
pip install pywin32
```

### Configurar pre-commit hooks

```Bash
pipenv run pre-commit install
```

### Rodar aplicação Local

```Bash
pipenv run app
```

### Comandos de Testes

```Bash
pipenv run test     # Sem cobertura
pipenv run test:cov # Com cobertura
```

### Qualidade de código

```Bash
pipenv run precommit
```

### Setup do banco

```Bash
pipenv run migrate  # Aplicar migrations (alembic upgrade head)
pipenv run seed     # Popular dados iniciais
pipenv run app      # Rodar aplicação
```

### Banco Local

- Usa PostgreSQL

### Comandos Úteis

```bash
# Migrations (se necessário)
alembic revision --autogenerate -m "nome_da_migration"      # Nova migration (detecta mudanças automaticamente)
alembic upgrade head                                        # Aplicar todas as migrations pendentes
alembic current                                             # Ver migration atual
alembic history                                             # Ver histórico de migrations
alembic revision -m "nome_da_migration"                     # Criar migration manual
alembic downgrade -1                                        # Reverter para migration anterior
alembic downgrade <revision_id>                             # Reverter para migration específica
```

**Exemplos de nomes de migration:**

```bash
alembic revision --autogenerate -m "create_users_table"
alembic revision --autogenerate -m "add_email_column_to_users"
alembic revision --autogenerate -m "create_indexes_for_performance"
```

## Desenvolvimento com Docker

### Rodar Docker do Projeto

```Bash
docker compose up --build

docker compose down # Parar containers
```

### Banco

```Bash
# Apenas banco
docker compose up db

# Aplicar migrations
docker compose run --rm migrate

# Executar seed
docker compose run --rm seed
```

### Ferramentas de Qualidade

```Bash
# Testes
docker compose run --rm test
docker compose run --rm test-cov

# Qualidade de código
docker compose run --rm quality
```

### Acessar Banco PostgreSQL

#### 1. Conectar ao container do banco

```bash
docker compose exec db psql -U admin -d bah_db # Necessário ter o container do banco rodando
```

#### 2. Comandos dentro do PostgreSQL

```sql
# Listar todas as tabelas
\dt

# Ver dados da tabela
SELECT * FROM <nome_tabela>;

# Ver estrutura da tabela
\d <nome_tabela>

# Ver informações do banco
\l

# Ver todos os esquemas
\dn

# Sair do PostgreSQL
\q
```

#### 3. Verificar se o container está rodando

```bash
docker compose ps
```

### Interface Web para Banco de Dados

#### Adminer

Para acessar o Adminer é preciso estar com o Docker rodando

- **URL**: http://localhost:8080
- **Sistema**: PostgreSQL
- **Servidor**: db
- **Usuário**: admin
- **Senha**: admin
- **Base de dados**: bah_db

## API Endpoints

A API FastAPI já vem configurada com Swagger e pronta para uso

### Documentação Geral

Com a aplicação rodando, acesse:
- **Swagger UI**: http://localhost:8000/
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Arquitetura do Projeto

### Estrutura de Pastas

```
bah-backend/
├── app/                          # Código principal da aplicação
│   ├── config/                   # Configurações (banco, settings)
│   │   └── database.py          # Configuração do SQLAlchemy
│   ├── controllers/             # Controladores (lógica de apresentação)
│   ├── models/                  # Modelos SQLAlchemy (entidades do banco)
│   ├── repositories/            # Camada de acesso a dados
│   ├── routes/                  # Definição das rotas FastAPI
│   ├── schemas/                 # Schemas Pydantic (validação/serialização)
│   ├── services/                # Regras de negócio
│   ├── scripts/                 # Scripts utilitários (seed, etc)
│   ├── utils/                   # Funções auxiliares
│   └── main.py                  # Ponto de entrada da aplicação
├── migrations/                   # Migrations do Alembic
├── tests/                       # Testes automatizados
│   ├── integration/             # Testes de integração
│   └── conftest.py             # Configurações dos testes
├── docker-compose.yml           # Orquestração de containers
├── Dockerfile                   # Imagem Docker da aplicação
├── Pipfile                      # Dependências Python (pipenv)
└── pyproject.toml              # Configurações de ferramentas
```

### Padrão de Arquitetura (Clean Architecture)

O projeto segue uma arquitetura em camadas inspirada na Clean Architecture:

#### 1. **Routes** (Camada de Apresentação)

- Define os endpoints da API
- Recebe requisições HTTP
- Valida dados de entrada via Pydantic
- Chama os Controllers

#### 2. **Controllers** (Camada de Controle)

- Orquestra as operações
- Gerencia dependências (injeção do banco)
- Chama os Services
- Trata respostas para a API

#### 3. **Services** (Camada de Negócio)

- Contém as regras de negócio
- Validações específicas do domínio
- Orquestra chamadas aos Repositories
- Trata exceções de negócio

#### 4. **Repositories** (Camada de Dados)

- Acesso direto ao banco de dados
- Operações CRUD
- Queries específicas
- Abstrai detalhes do SQLAlchemy

#### 5. **Models** (Entidades)

- Definição das tabelas (SQLAlchemy)
- Relacionamentos entre entidades
- Constraints do banco

#### 6. **Schemas** (Contratos de Dados)

- Validação de entrada (Pydantic)
- Serialização de saída
- Documentação automática da API

### Fluxo de uma Requisição

```
1. Cliente HTTP → Route (FastAPI)
2. Route → Controller (injeção de dependências)
3. Controller → Service (regras de negócio)
4. Service → Repository (acesso aos dados)
5. Repository → Database (SQLAlchemy)
6. Database → Repository → Service → Controller → Route → Cliente
```

## 🔧 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **Alembic**: Migrations de banco de dados
- **Pydantic**: Validação e serialização de dados
- **PostgreSQL**: Banco de dados principal (produção)
- **PostgreSQL**: Banco de dados local (desenvolvimento)
- **Docker**: Containerização
- **Pytest**: Framework de testes
- **Black/isort**: Formatação de código
- **Pylint**: Análise estática de código

## 📋 Como Contribuir

### Implementar (seguindo a arquitetura)

1. **Model** - Definir entidade no banco
2. **Schema** - Criar contratos Pydantic
3. **Repository** - Implementar acesso aos dados
4. **Service** - Adicionar regras de negócio
5. **Controller** - Orquestrar operações
6. **Route** - Expor endpoints
7. **Tests** - Criar testes unitários e integração

### Padrões de Código

#### Nomenclatura

- **Arquivos**: `snake_case.py`
- **Classes**: `PascalCase`
- **Funções/Variáveis**: `snake_case`
- **Constantes**: `UPPER_CASE`

### 4. Checklist de Contribuição

- [ ] Código segue os padrões estabelecidos
- [ ] Testes criados e passando (cobertura > 80%)
- [ ] Documentação atualizada se necessário
- [ ] Migration criada se houver mudanças no banco
- [ ] Pre-commit hooks passando
- [ ] Branch atualizada com `dev`
- [ ] Pull Request com descrição clara

## 🚀 Deploy e Ambientes

### Desenvolvimento Local

- PostgreSQL como banco
- Servidor de desenvolvimento do uvicorn
- Hot reload ativado

### Testes

- Banco em memória
- Fixtures para dados de teste
- Isolamento entre testes

### Produção (Docker)

- PostgreSQL como banco
- Containers orquestrados
- Migrations automáticas
- Health checks configurados

## � Git Flow

### Estrutura de Branches

- `main` - Branch principal (produção)
- `dev` - Branch de desenvolvimento
- `feature/nome-da-funcionalidade` - Novas funcionalidades
- `bugfix/nome-do-bug` - Correções de bugs

### Fluxo de Trabalho

1. **Começar uma nova funcionalidade:**

```bash
# Ir para dev e pegar atualizações
git checkout dev
git pull origin dev

# Criar nova branch
git checkout -b feature/minha-funcionalidade
```

2. **Fazer commits:**

```bash
# Adicionar arquivos modificados
git add .

# Fazer commit com mensagem descritiva
git commit -m "feat: adicionar componente de login"
```

3. **Enviar para o repositório:**

```bash
git push origin feature/minha-funcionalidade
```

4. **Criar Pull Request:**

- Acesse o GitHub/GitLab
- Clique em "New Pull Request"
- Aponte para a branch `dev`
- Descreva as alterações
- Aguarde revisão

### Tipos de Commit (Convenção)

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação de código
- `refactor:` - Refatoração
- `test:` - Testes

**Exemplos:**

```bash
git commit -m "feat: adicionar botão de salvar"
git commit -m "fix: corrigir validação do formulário"
git commit -m "docs: atualizar README"
```

### Comandos Git Essenciais

```bash
git status                    # Ver arquivos modificados
git add .                     # Adicionar todos os arquivos
git add arquivo.txt           # Adicionar arquivo específico
git commit -m "mensagem"      # Fazer commit
git push                      # Enviar para repositório
git pull                      # Baixar atualizações
git checkout branch-name      # Trocar de branch
git branch                    # Listar branches
git branch -d branch-name     # Deletar branch local
```

## 📚 Recursos Úteis

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

---

💡 **Dica:** Sempre teste suas alterações localmente antes de fazer push!
