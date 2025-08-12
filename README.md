# React + TypeScript + Vite + Tailwind CSS + shadcn/ui

Este projeto é um template moderno para desenvolvimento web usando as tecnologias mais atuais disponíveis.

## 🚀 Stack Tecnológica

- **React 19** - Biblioteca para construção de interfaces de usuário
- **TypeScript** - Superset tipado do JavaScript
- **Vite** - Build tool e servidor de desenvolvimento ultra-rápido
- **Tailwind CSS v4** - Framework CSS utility-first
- **shadcn/ui** - Coleção de componentes UI reutilizáveis e acessíveis
- **ESLint** - Ferramenta de linting para manter a qualidade do código

## 📦 Instalação

```bash
npm install
```

## 🛠️ Scripts Disponíveis

```bash
# Executar servidor de desenvolvimento
npm run dev

# Fazer build para produção
npm run build

# Visualizar build de produção
npm run preview

# Executar linting
npm run lint
```

## 🎨 Tailwind CSS v4

Este projeto usa o Tailwind CSS v4 com as seguintes configurações:

- **PostCSS Plugin**: `@tailwindcss/postcss`
- **Configuração**: `tailwind.config.js`
- **CSS Principal**: `src/index.css`

## 🧩 shadcn/ui

O projeto está configurado com shadcn/ui incluindo:

- **Componentes instalados**: Button, Card
- **Utilitários**: Função `cn()` para merge de classes CSS
- **Tema**: New York style com cor base Neutral
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
