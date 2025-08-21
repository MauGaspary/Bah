# Bah – Plataforma de Inovação de Caxias do Sul

## Desenvolvimento Local

### Instalar dependências

```Bash
pip install pipenv

pipenv install --dev
```

### Ativar virtual environment

#### Mac e Linux

```Bash
source .venv/bin/activate
```

#### Windows

```Shell
.venv\Scripts\activate
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

pipenv run format:all

pipenv run lint:all

pipenv run pylint:all
```

## Docker

### Rodar aplicação com Docker

```Bash
docker compose up --build
```

### Testes no Docker

```Bash
docker compose run --rm test

# Testes com cobertura
docker compose run --rm test-cov
```

### Ferramentas de qualidade no Docker

```Bash
# Formatação de código
docker compose run --rm format

# Análise de código
docker compose run --rm lint

# Verificação de tipos
docker compose run --rm mypy

# Todas as verificações anteriores em um só comando
docker compose run --rm quality
```

### Testes + qualidade (pipeline completo)

```Bash
docker compose run --rm ci
```

### Parar aplicação

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

## 📁 Estrutura do Projeto

```
src/
├── components/
│   └── ui/              # Componentes do design system
├── lib/
│   └── utils.ts         # Funções utilitárias
├── assets/              # Imagens, ícones, etc.
├── App.tsx             # Componente principal
├── main.tsx            # Ponto de entrada
└── index.css           # Estilos globais + tokens BAH
```

## 📚 Recursos Úteis

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com/docs/components)
- [Lucide Icons](https://lucide.dev/icons/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)
- [React Docs](https://react.dev/)

---

💡 **Dica:** Sempre teste suas alterações localmente antes de fazer push!
