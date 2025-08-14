# BAH Frontend

Aplicação **Comandos Docker disponíveis:**

````bash
# Desenvolvimento
npm run docker:dev                 # Sobe o container em background (recomendado)
npm run docker:dev:attached       # Sobe o container "grudado" no terminal
npm run docker:stop               # Pausa os containers (mantém dados)
npm run docker:down               # Para e remove containers (mantém imagens)
npm run docker:logs               # Visualiza logs do frontend
npm run docker:shell              # Acessa shell do container

# Limpeza
npm run docker:clean              # Remove TUDO (containers, volumes, imagens)
```projeto BAH desenvolvida com React, TypeScript, Vite e Tailwind CSS.

## 🚀 Métodos de Desenvolvimento

Você pode escolher entre **duas formas** de rodar o projeto:

### 📦 Método 1: Docker (Recomendado para novos desenvolvedores)

**Pré-requisitos:**
- Docker
- Docker Compose

**Configuração rápida:**
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd bah-frontend

# Suba o ambiente Docker
npm run docker:dev

# Acesse: http://localhost:5173
````

**Comandos Docker disponíveis:**

```bash
# Desenvolvimento
npm run docker:dev                 # Sobe o container em modo desenvolvimento
npm run docker:dev:detached       # Suba em background (detached)
npm run docker:stop               # Para os containers
npm run docker:logs               # Visualiza logs do frontend
npm run docker:shell              # Acessa shell do container

# Limpeza
npm run docker:clean              # Remove containers, volumes e imagens
```

### 💻 Método 2: Desenvolvimento Local

**Pré-requisitos:**

- Node.js 24+
- npm ou yarn

**Configuração:**

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd bah-frontend

# Instale dependências
npm install

# Rode em desenvolvimento
npm run dev

# Acesse: http://localhost:5173
```

**Comandos disponíveis:**

```bash
npm run dev        # Servidor de desenvolvimento
npm run build      # Build para produção
npm run preview    # Preview do build
npm run lint       # Verificar código
npm run lint:fix   # Corrigir problemas do linter
```

## 🎨 Design System

O projeto usa tokens de design personalizados definidos em `src/index.css`:

### Cores BAH

- `bg-bah-blue` - Azul principal (#41edee)
- `bg-bah-green` - Verde (#c7d871)
- `bg-bah-purple` - Roxo (#542e82)
- `bg-bah-red` - Vermelho (#fe716f)

### Fontes

- `font-kanit` - Títulos e destaques
- `font-sf-pro` - Texto geral
- `font-mulish` - Alternativa

### Componentes

- **Button**: Componente padrão com variantes `primary`, `success`, `secondary`, `purple`
- **Card**: Layout de cartões com bordas arredondadas

## 🔄 Fluxo de Desenvolvimento Docker

```bash
# 🌅 Começar o dia / sessão de desenvolvimento
npm run docker:dev              # Roda em background, libera o terminal

# 💻 Desenvolver normalmente...
# Ver logs se necessário
npm run docker:logs             # Em outro terminal ou aba

# 🔍 Debug se precisar
npm run docker:shell            # Acessa o container

# 🌙 Parar temporariamente (mantém tudo)
npm run docker:stop             # Pausa, dados preservados

# 🔄 Continuar de onde parou
npm run docker:dev              # Retoma rapidamente

# 🧹 Limpeza completa (quando algo der errado)
npm run docker:clean            # Remove tudo, recomeça do zero
```

- **Ícones**: Lucide React

### Adicionando novos componentes:

```bash
npx shadcn@latest add [nome-do-componente]
```

Exemplos:

```bash
npx shadcn@latest add input
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
```

## 📁 Estrutura do Projeto

```
src/
├── components/
│   └── ui/              # Componentes shadcn/ui
├── lib/
│   └── utils.ts         # Utilitários (função cn)
├── assets/              # Recursos estáticos
├── App.tsx             # Componente principal
├── main.tsx            # Ponto de entrada
└── index.css           # Estilos globais + Tailwind
```

## 🔧 Configurações

### TypeScript

- Path mapping configurado (`@/*` → `./src/*`)
- Configuração em `tsconfig.app.json` e `tsconfig.json`

### Vite

- Alias de importação configurado
- Plugin React habilitado

### PostCSS

- Plugin Tailwind CSS v4
- Autoprefixer para compatibilidade entre browsers

## 📖 Exemplos de Uso

### Usando componentes shadcn/ui:

```tsx
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

function ExampleComponent() {
  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Título do Card</CardTitle>
        <CardDescription>Descrição do card</CardDescription>
      </CardHeader>
      <CardContent>
        <Button variant="default" size="lg">
          Clique aqui
        </Button>
      </CardContent>
    </Card>
  );
}
```

### Usando Tailwind CSS:

```tsx
function ResponsiveLayout() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">
          Layout Responsivo
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Conteúdo */}
        </div>
      </div>
    </div>
  );
}
```

## 🎯 Próximos Passos

1. **Adicionar mais componentes**: Explore a [documentação do shadcn/ui](https://ui.shadcn.com/docs)
2. **Configurar tema personalizado**: Customize as cores e estilos no `tailwind.config.js`
3. **Adicionar testes**: Considere usar Vitest + Testing Library
4. **Configurar CI/CD**: Setup para deploy automatizado

## 📚 Recursos Úteis

- [Documentação do Tailwind CSS v4](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com/docs/components)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Documentation](https://react.dev/)

## 🔧 Configuração Avançada do ESLint

Para aplicações em produção, você pode configurar regras de lint mais rigorosas. Consulte a [documentação do ESLint](https://eslint.org/docs) para mais detalhes.

## 📋 Versões das Dependências

- **React**: ^19.1.1
- **TypeScript**: ~5.8.3
- **Vite**: ^7.1.0
- **Tailwind CSS**: ^4.1.11
- **shadcn/ui**: Mais recente
