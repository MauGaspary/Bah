# Como Executar os Testes de Login

## Passo a Passo

### 1. Iniciar o Servidor de Desenvolvimento

```bash
npm run dev
```

Certifique-se de que o servidor está rodando em `http://localhost:5173`

### 2. Executar os Testes

#### Opção A: Modo Interativo (Recomendado para desenvolvimento)

```bash
npm run cypress:open
```

- Abre o Cypress Test Runner
- Permite executar testes individualmente
- Mostra a interface visual dos testes
- Ideal para debug e desenvolvimento

#### Opção B: Modo Headless (Recomendado para CI/CD)

```bash
npm run cypress:run
```

- Executa todos os testes em modo headless
- Mostra resultados no terminal
- Mais rápido para execução automatizada

### 3. Executar Apenas o Teste de Login

```bash
npx cypress run --spec "cypress/e2e/login.cy.ts"
```

### 4. Executar com Navegador Específico

```bash
npx cypress run --browser chrome
npx cypress run --browser firefox
npx cypress run --browser edge
```

## Estrutura dos Testes Criados

### Arquivos Criados:

- `cypress/e2e/login.cy.ts` - Teste principal da tela de login
- `cypress/fixtures/login.json` - Dados de teste
- `cypress/support/commands.ts` - Comandos customizados
- `cypress.config.ts` - Configuração atualizada
- `package.json` - Scripts adicionados

### Testes Incluídos:

1. **Exibição de elementos** - Verifica se todos os elementos estão presentes
2. **Validação de campos** - Testa validação de campos obrigatórios
3. **Validação de email** - Testa formato de email inválido
4. **Toggle de senha** - Testa mostrar/ocultar senha
5. **Limpeza de email** - Testa botão X para limpar campo
6. **Checkbox Remember Me** - Testa funcionalidade do checkbox
7. **Login válido** - Testa login com credenciais corretas
8. **Login inválido** - Testa tratamento de credenciais incorretas
9. **Estado de loading** - Testa indicador de carregamento
10. **Erro de rede** - Testa tratamento de erros de conexão
11. **Responsividade** - Testa em dispositivos móveis
12. **Acessibilidade** - Testa navegação por teclado

## Comandos Customizados Disponíveis

```typescript
// Login rápido
cy.login('email@test.com', 'password123')

// Limpar autenticação
cy.clearAuth()

// Definir token de autenticação
cy.setAuthToken('mock-jwt-token')

// Verificar se está autenticado
cy.isAuthenticated()
```

## Dados de Teste

Os dados de teste estão em `cypress/fixtures/login.json`:

```json
{
  "validUser": {
    "email": "admin@test.com",
    "password": "password123"
  },
  "invalidUser": {
    "email": "invalid@test.com",
    "password": "wrongpassword"
  },
  "invalidEmail": {
    "email": "invalid-email",
    "password": "password123"
  },
  "emptyFields": {
    "email": "",
    "password": ""
  }
}
```

## Troubleshooting

### Erro: "Cannot connect to localhost:5173"

- Certifique-se de que o servidor está rodando: `npm run dev`
- Verifique se a porta 5173 está disponível

### Testes falhando por timeout

- Aumente os timeouts em `cypress.config.ts` se necessário
- Verifique se a aplicação está carregando corretamente

### Elementos não encontrados

- Verifique se os seletores CSS estão corretos
- Aguarde a página carregar completamente antes de interagir

### Problemas de autenticação

- Use `cy.clearAuth()` antes de cada teste
- Verifique se os mocks de API estão configurados corretamente
