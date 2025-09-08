# Bah – Plataforma de Inovação de Caxias do Sul

## Desenvolvimento Local

### Instalar pipenv

```Bash
pip install pipenv
```

### Ativar virtual environment

```Bash
python -m venv .venv
```

#### Mac e Linux

```Bash
source .venv/bin/activate
```

#### Windows

```Shell
.venv\Scripts\activate
```

### Instalar dependências do projeto

```Bash
pipenv install --dev
```

### Configurar pre-commit hooks

```Bash
pipenv run pre-commit install
```

### Rodar aplicação Local

```Bash
pipenv run app
```

### Testes

```Bash
pipenv run test
pipenv run test:cov
```

#### Helpers de Teste

O projeto inclui helpers para padronizar requests nos testes:

```python
from tests.helpers import request, request_auth

# Request básico
response = request(client, "POST", "/admin/", json=data)

# Request autenticado
response = request_auth(client, "GET", "/admin/protected", token="jwt-token")
```

Veja [TESTING.md](TESTING.md) para documentação completa.

### Qualidade de código

```Bash
pipenv run precommit
```

### Setup do banco

```Bash
pipenv run migrate
pipenv run seed
pipenv run app
```

### Banco Local

- Usa SQLite (`bah.db`) no diretório raiz

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

# Seed
pipenv run seed             # Popular dados iniciais
```

**Exemplos de nomes de migration:**

```bash
alembic revision --autogenerate -m "create_users_table"
alembic revision --autogenerate -m "add_email_column_to_users"
alembic revision --autogenerate -m "create_indexes_for_performance"
```

## Desenvolvimento com Docker

### Rodar App

```Bash
docker compose up --build
```

### Serviços Individuais

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
docker compose exec db psql -U bah_user -d bah_db
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

Se o container não estiver rodando, inicie com:

```bash
docker compose up db -d
```

### Configuração do Banco (Docker)

- **Host**: localhost:5432
- **Database**: bah_db
- **User**: bah_user
- **Password**: bah_password

### Interface Web para Banco de Dados

O projeto inclui duas opções de UI para visualizar e gerenciar o banco:

#### 1. Adminer

```bash
# Iniciar com o banco
docker compose up db adminer -d
```

- **URL**: http://localhost:8080
- **Sistema**: PostgreSQL
- **Servidor**: db
- **Usuário**: bah_user
- **Senha**: bah_password
- **Base de dados**: bah_db

#### 2. pgAdmin

```bash
# Iniciar com o banco
docker compose up db pgadmin -d
```

- **URL**: http://localhost:8081
- **Email**: admin@bah.com.br
- **Senha**: admin123

Depois adicione o servidor PostgreSQL:
- **Host**: db
- **Port**: 5432
- **Database**: bah_db
- **Username**: bah_user
- **Password**: bah_password

## Parar Docker

```Bash
docker compose down
```

## API Endpoints

A API FastAPI já vem configurada e pronta para uso. Com a aplicação rodando:

### Documentação Geral

Com a aplicação rodando, acesse:
- **Swagger UI**: http://localhost:8000/
- **ReDoc**: http://localhost:8000/redoc

### Dados de Seed

- admin@bah.com.br
- joao.silva@bah.com.br
- maria.santos@bah.com.br

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

### Exemplo Prático: Criar Admin

```python
# 1. Route recebe a requisição
@router.post("/", response_model=AdminResponse)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    controller = AdminController(db)
    return controller.create_admin(admin)

# 2. Controller orquestra
class AdminController:
    def create_admin(self, admin_data: AdminCreate) -> AdminResponse:
        return self.service.create_admin(admin_data)

# 3. Service aplica regras de negócio
class AdminService:
    def create_admin(self, admin_data: AdminCreate):
        if not validate_email(admin_data.email):
            raise HTTPException(status_code=400, detail="Email inválido")
        return self.repository.create(admin_data)

# 4. Repository acessa o banco
class AdminRepository:
    def create(self, admin_data: AdminCreate):
        db_admin = Admin(username=admin_data.username, email=admin_data.email)
        self.db.add(db_admin)
        self.db.commit()
        return db_admin
```

## 🔧 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **Alembic**: Migrations de banco de dados
- **Pydantic**: Validação e serialização de dados
- **PostgreSQL**: Banco de dados principal (produção)
- **SQLite**: Banco de dados local (desenvolvimento)
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

### Migration (se necessário)

```bash
# Criar migration
alembic revision --autogenerate -m "descrição_da_mudança"

# Aplicar migration
pipenv run migrate
```

### 3. Padrões de Código

#### Nomenclatura

- **Arquivos**: `snake_case.py`
- **Classes**: `PascalCase`
- **Funções/Variáveis**: `snake_case`
- **Constantes**: `UPPER_CASE`

#### Estrutura de Arquivos

```python
from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Exemplo(Base):
    __tablename__ = "exemplos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
```

#### Testes

```python
def test_criar_exemplo(client):
    response = client.post("/exemplo/", json={"nome": "teste"})
    assert response.status_code == 201
    assert response.json()["nome"] == "teste"
```

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

- SQLite como banco
- Servidor de desenvolvimento do uvicorn
- Hot reload ativado

### Testes

- Banco em memória (SQLite)
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
