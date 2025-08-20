# Innovation Search API com IA


# Instalar dependências local

É preciso ter o python e o pip instalado

```
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

# Rodar aplicação
```
uvicorn app.main:app --reload
```


# Comando de teste
```
pytest tests/test_admin_example.py -v
```


# Docker

## Rodar com Docker Compose
```
docker compose up --build
ou
docker compose up --build -d
```

## Parar e remover containers
```
docker compose down  
````

## Rodar apenas o app
```
docker build -t bah-backend .
docker run -p 8000:8000 bah-backend
```





# Migrations

## Gerar nova migration
```
alembic revision --autogenerate -m "description"
```

## Aplicar migrations
```
alembic upgrade head
```

## Reverter migration
```
alembic downgrade -1
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
