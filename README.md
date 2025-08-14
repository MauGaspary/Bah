# BAH Frontend

Frontend do projeto BAH desenvolvido com tecnologias modernas para uma experiência de desenvolvimento eficiente e produtiva.

## 🛠️ Tecnologias

- **React 19** - Biblioteca para interfaces de usuário
- **TypeScript** - JavaScript com tipagem estática
- **Vite** - Build tool moderna e rápida
- **Tailwind CSS v4** - Framework CSS utilitário
- **shadcn/ui** - Componentes acessíveis e customizáveis
- **Lucide React** - Biblioteca de ícones
- **Docker** - Containerização para desenvolvimento

## � Iniciando o Desenvolvimento

### Pré-requisitos

- Docker e Docker Compose instalados
- Git configurado

### Passo a Passo

1. **Clone o repositório:**

```bash
git clone <url-do-repositorio>
cd bah-frontend
```

2. **Execute o setup automático (APENAS NA PRIMEIRA VEZ):**

```bash
chmod +x setup.sh
./setup.sh
```

- Escolha "1" para Docker (recomendado)
- O script vai verificar dependências e configurar tudo automaticamente

3. **Acesse a aplicação:**

- Frontend: http://localhost:5173

> **⚠️ IMPORTANTE:** O `setup.sh` é APENAS para quem acabou de clonar o repositório. No dia a dia, use simplesmente `npm run docker:dev`!

### Comandos Docker Disponíveis

**Para uso diário (após o primeiro setup):**

```bash
npm run docker:dev                 # Sobe em background (comando do dia a dia)
npm run docker:stop               # Pausa containers (mantém dados)
npm run docker:logs               # Visualiza logs
```

**Comandos adicionais:**

```bash
npm run docker:dev:attached       # Sobe "grudado" no terminal (debug)
npm run docker:down               # Para e remove containers
npm run docker:shell              # Acessa shell do container
npm run docker:clean              # Remove TUDO (emergência)
```

## 🎨 Design System

### Tokens de Design (BAH)

**Cores principais:**

- `bg-bah-blue` - Azul BAH (#41edee)
- `bg-bah-green` - Verde BAH (#c7d871)
- `bg-bah-purple` - Roxo BAH (#542e82)
- `bg-bah-red` - Vermelho BAH (#fe716f)

**Tipografia:**

- `font-kanit` - Títulos e destaques
- `font-sf-pro` - Texto geral
- `font-mulish` - Texto alternativo

### Componentes Disponíveis

**Button (Botão):**

```tsx
import { Button } from '@/components/ui/button'

<Button variant="primary">Primário</Button>
<Button variant="success">Sucesso</Button>
<Button variant="secondary">Secundário</Button>
<Button variant="purple">Roxo</Button>
```

**Card (Cartão):**

```tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

;<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
  </CardHeader>
  <CardContent>Conteúdo do card</CardContent>
</Card>
```

### Adicionando Novos Componentes

```bash
npx shadcn@latest add input
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
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
