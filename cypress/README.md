# Testes E2E com Cypress - BAH Frontend

Este diretório contém os testes end-to-end (E2E) para o frontend do projeto BAH, utilizando Cypress.

## Estrutura

```
cypress/
├── e2e/                    # Testes E2E
│   └── login.cy.ts        # Testes da tela de login
├── fixtures/              # Dados de teste
│   ├── example.json       # Exemplo de fixture
│   └── login.json         # Dados para testes de login
├── support/               # Arquivos de suporte
│   ├── commands.ts        # Comandos customizados
│   └── e2e.ts            # Configuração global
└── downloads/             # Downloads dos testes
```

## Testes Disponíveis

### Login (`login.cy.ts`)

Testa a funcionalidade completa da tela de login, incluindo:

- ✅ Exibição correta dos elementos da página
- ✅ Validação de campos obrigatórios
- ✅ Validação de formato de email
- ✅ Toggle de visibilidade da senha
- ✅ Limpeza do campo de email
- ✅ Funcionamento do checkbox "Remember Me"
- ✅ Login com credenciais válidas
- ✅ Tratamento de credenciais inválidas
- ✅ Estado de loading durante o login
- ✅ Tratamento de erros de rede
- ✅ Responsividade em dispositivos móveis
- ✅ Navegação por teclado (acessibilidade)

## Como Executar os Testes

### Pré-requisitos

1. Certifique-se de que o servidor de desenvolvimento está rodando:

   ```bash
   npm run dev
   ```

2. O servidor deve estar disponível em `http://localhost:5173`

### Executar Testes

#### Modo Interativo (Cypress Test Runner)

```bash
npm run cypress:open
# ou
npm run test:e2e:open
```

#### Modo Headless (linha de comando)

```bash
npm run cypress:run
# ou
npm run test:e2e
```

#### Modo Headless com navegador específico

```bash
npx cypress run --browser chrome
npx cypress run --browser firefox
npx cypress run --browser edge
```

## Comandos Customizados

O projeto inclui comandos customizados para facilitar os testes:

- `cy.login(email, password)` - Realiza login com as credenciais fornecidas
- `cy.clearAuth()` - Remove o token de autenticação do localStorage
- `cy.setAuthToken(token)` - Define um token de autenticação no localStorage
- `cy.isAuthenticated()` - Verifica se o usuário está autenticado

## Fixtures

### login.json

Contém dados de teste para diferentes cenários de login:

- `validUser` - Credenciais válidas para login bem-sucedido
- `invalidUser` - Credenciais inválidas para testar falha de autenticação
- `invalidEmail` - Email com formato inválido
- `emptyFields` - Campos vazios para testar validação

## Configuração

A configuração do Cypress está em `cypress.config.ts` e inclui:

- Base URL: `http://localhost:5173`
- Viewport padrão: 1280x720
- Timeouts configurados para 10 segundos
- Screenshots automáticas em caso de falha
- Vídeos desabilitados para melhor performance

## Interceptação de Requisições

Os testes utilizam `cy.intercept()` para mockar as requisições da API, permitindo:

- Simular respostas de sucesso e erro
- Testar diferentes cenários sem depender do backend
- Controlar o timing das respostas
- Simular erros de rede

## Boas Práticas

1. **Isolamento**: Cada teste é independente e limpa o estado antes de executar
2. **Dados de Teste**: Utilize fixtures para dados consistentes
3. **Seletores**: Prefira seletores semânticos (data-testid, aria-label, etc.)
4. **Aguardar**: Use `cy.wait()` para aguardar requisições quando necessário
5. **Assertions**: Seja específico nas verificações de estado

## Troubleshooting

### Testes falhando por timeout

- Verifique se o servidor de desenvolvimento está rodando
- Aumente os timeouts na configuração se necessário

### Elementos não encontrados

- Verifique se os seletores estão corretos
- Aguarde a página carregar completamente antes de interagir

### Problemas de autenticação

- Use `cy.clearAuth()` antes de cada teste
- Verifique se os tokens mockados estão corretos

## Contribuindo

Ao adicionar novos testes:

1. Siga a convenção de nomenclatura: `feature.cy.ts`
2. Adicione fixtures necessárias em `cypress/fixtures/`
3. Use comandos customizados quando apropriado
4. Documente novos comandos em `commands.ts`
5. Mantenha os testes independentes e determinísticos
