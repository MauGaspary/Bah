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

```Bash
# Migrations
pipenv run migrate:create   # Nova migration
pipenv run migrate          # Aplicar migrations
pipenv run migrate:current  # Status
pipenv run migrate:history  # Histórico

# Seed
pipenv run seed             # Popular dados iniciais
```

## Desenvolvimento com Docker

### Rodar App

```Bash
docker compose up --build

# Testar endpoints
bash test_endpoints.sh
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

### Configuração do Banco (Docker)

- **Host**: localhost:5432
- **Database**: bah_db
- **User**: bah_user
- **Password**: bah_password

## Parar Docker

```Bash
docker compose down
```

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

## API Endpoints

Com a aplicação rodando:

```bash
# Listar admins
curl http://localhost:8000/admin/

# Criar admin
curl -X POST http://localhost:8000/admin/ \
  -H "Content-Type: application/json" \
  -d '{"username": "novo.admin", "email": "novo@bah.com.br"}'

# Buscar por ID
curl http://localhost:8000/admin/id/1

# Buscar por email
curl http://localhost:8000/admin/email/admin@bah.com.br
```

### Dados de Seed

- admin@bah.com.br
- joao.silva@bah.com.br
- maria.santos@bah.com.br

## 📚 Recursos Úteis

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

---

💡 **Dica:** Sempre teste suas alterações localmente antes de fazer push!
