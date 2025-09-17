/// <reference types="cypress" />

describe('Login Page Tests', () => {
  beforeEach(() => {
    // Visita a página de login antes de cada teste
    cy.visit('/admin')
  })

  it('should display login page elements correctly', () => {
    // Verifica se os elementos principais estão presentes
    cy.get('h1').should('contain', 'Login')
    cy.get('p').should('contain', 'Please fill your detail to access your account.')
    
    // Verifica se os campos de input estão presentes
    cy.get('input[type="email"]').should('be.visible')
    cy.get('input[type="password"]').should('be.visible')
    
    // Verifica se o botão de login está presente
    cy.get('button[type="submit"]').should('be.visible').and('contain', 'Sign in')
    
    // Verifica se o checkbox "Remember Me" está presente
    cy.get('input[type="checkbox"]').should('be.visible')
    
    // Verifica se a logo está presente
    cy.get('img[alt="BAH Logo"]').should('be.visible')
  })

  it('should show validation errors for empty fields', () => {
    // Tenta submeter o formulário sem preencher os campos
    cy.get('button[type="submit"]').click()
    
    // Verifica se as mensagens de validação aparecem
    cy.get('input[type="email"]:invalid').should('exist')
    cy.get('input[type="password"]:invalid').should('exist')
  })

  it('should show validation error for invalid email format', () => {
    cy.fixture('login').then((loginData) => {
      // Preenche com email inválido
      cy.get('input[type="email"]').type(loginData.invalidEmail.email)
      cy.get('input[type="password"]').type(loginData.invalidEmail.password)
      
      // Tenta submeter
      cy.get('button[type="submit"]').click()
      
      // Verifica se a mensagem de erro aparece
      cy.get('input[type="email"]:invalid').should('exist')
    })
  })

  it('should toggle password visibility', () => {
    cy.fixture('login').then((loginData) => {
      // Preenche a senha
      cy.get('input[type="password"]').type(loginData.validUser.password)
      
      // Verifica se inicialmente a senha está oculta
      cy.get('input[type="password"]').should('have.attr', 'type', 'password')
      
      // Clica no botão de mostrar/ocultar senha
      cy.get('button[aria-label="Show password"]').click()
      
      // Verifica se a senha agora está visível
      cy.get('input[type="text"]').should('be.visible')
      
      // Clica novamente para ocultar
      cy.get('button[aria-label="Hide password"]').click()
      
      // Verifica se a senha está oculta novamente
      cy.get('input[type="password"]').should('have.attr', 'type', 'password')
    })
  })

  it('should clear email field when X button is clicked', () => {
    cy.fixture('login').then((loginData) => {
      // Preenche o email
      cy.get('input[type="email"]').type(loginData.validUser.email)
      
      // Verifica se o botão X aparece
      cy.get('span[aria-label="Limpar email"]').should('be.visible')
      
      // Clica no botão X
      cy.get('span[aria-label="Limpar email"]').click()
      
      // Verifica se o campo foi limpo
      cy.get('input[type="email"]').should('have.value', '')
    })
  })

  it('should toggle remember me checkbox', () => {
    // Verifica estado inicial do checkbox
    cy.get('input[type="checkbox"]').should('not.be.checked')
    
    // Clica no checkbox
    cy.get('input[type="checkbox"]').click()
    
    // Verifica se foi marcado
    cy.get('input[type="checkbox"]').should('be.checked')
    
    // Clica novamente
    cy.get('input[type="checkbox"]').click()
    
    // Verifica se foi desmarcado
    cy.get('input[type="checkbox"]').should('not.be.checked')
  })

  it('should handle login with valid credentials', () => {
    cy.fixture('login').then((loginData) => {
      // Intercepta a requisição de login
      cy.intercept('POST', '**/auth/login', {
        statusCode: 200,
        body: {
          access_token: 'mock-jwt-token',
          user: {
            id: '1',
            email: loginData.validUser.email,
            name: 'Test User'
          }
        }
      }).as('loginRequest')

      // Preenche os campos com credenciais válidas
      cy.get('input[type="email"]').type(loginData.validUser.email)
      cy.get('input[type="password"]').type(loginData.validUser.password)
      
      // Submete o formulário
      cy.get('button[type="submit"]').click()
      
      // Verifica se a requisição foi feita
      cy.wait('@loginRequest')
      
      // Verifica se foi redirecionado para o dashboard
      cy.url().should('include', '/dashboard')
    })
  })

  it('should show error message for invalid credentials', () => {
    cy.fixture('login').then((loginData) => {
      // Intercepta a requisição de login com erro
      cy.intercept('POST', '**/auth/login', {
        statusCode: 401,
        statusText: 'Unauthorized'
      }).as('loginError')

      // Preenche os campos com credenciais inválidas
      cy.get('input[type="email"]').type(loginData.invalidUser.email)
      cy.get('input[type="password"]').type(loginData.invalidUser.password)
      
      // Submete o formulário
      cy.get('button[type="submit"]').click()
      
      // Verifica se a requisição foi feita
      cy.wait('@loginError')
      
      // Verifica se a mensagem de erro aparece (baseada no erro real da função)
      cy.get('.text-red-500').should('be.visible').and('contain', 'Login failed: 401 Unauthorized')
      
      // Verifica se ainda está na página de login
      cy.url().should('include', '/admin')
    })
  })

  it('should show loading state during login', () => {
    cy.fixture('login').then((loginData) => {
      // Intercepta a requisição de login com delay
      cy.intercept('POST', '**/auth/login', {
        statusCode: 200,
        body: {
          access_token: 'mock-jwt-token',
          user: {
            id: '1',
            email: loginData.validUser.email,
            name: 'Test User'
          }
        },
        delay: 1000
      }).as('loginRequest')

      // Preenche os campos
      cy.get('input[type="email"]').type(loginData.validUser.email)
      cy.get('input[type="password"]').type(loginData.validUser.password)
      
      // Submete o formulário
      cy.get('button[type="submit"]').click()
      
      // Verifica se o botão mostra estado de loading
      cy.get('button[type="submit"]').should('contain', 'Signing in...')
      cy.get('button[type="submit"]').should('be.disabled')
      
      // Aguarda a requisição completar
      cy.wait('@loginRequest')
    })
  })

  it('should handle network error gracefully', () => {
    cy.fixture('login').then((loginData) => {
      // Intercepta a requisição de login e simula um erro de rede
      cy.intercept('POST', '**/auth/login', {
        statusCode: 0, // Status 0 indica erro de rede
        body: {},
        delay: 100
      }).as('networkError')

      // Preenche os campos
      cy.get('input[type="email"]').type(loginData.validUser.email)
      cy.get('input[type="password"]').type(loginData.validUser.password)
      
      // Submete o formulário
      cy.get('button[type="submit"]').click()
      
      // Aguarda a requisição
      cy.wait('@networkError')
      
      // Verifica se a mensagem de erro aparece
      cy.get('.text-red-500').should('be.visible')
      cy.get('.text-red-500').should('contain.text', 'Token ausente')
      
      // Verifica se ainda está na página de login
      cy.url().should('include', '/admin')
    })
  })

  it('should be accessible with keyboard navigation', () => {
    // Testa se os elementos são focáveis e têm os atributos de acessibilidade corretos
    cy.get('input[type="email"]').should('be.visible').and('have.attr', 'type', 'email')
    cy.get('input[type="password"]').should('be.visible').and('have.attr', 'type', 'password')
    cy.get('input[type="checkbox"]').should('be.visible').and('have.attr', 'type', 'checkbox')
    cy.get('button[type="submit"]').should('be.visible').and('have.attr', 'type', 'submit')
    
    // Testa foco nos elementos principais
    cy.get('input[type="email"]').focus()
    cy.get('input[type="email"]').should('be.focused')
    
    cy.get('input[type="password"]').focus()
    cy.get('input[type="password"]').should('be.focused')
    
    cy.get('input[type="checkbox"]').focus()
    cy.get('input[type="checkbox"]').should('be.focused')
    
    cy.get('button[type="submit"]').focus()
    cy.get('button[type="submit"]').should('be.focused')
    
    // Testa se o botão de mostrar/ocultar senha tem aria-label
    cy.get('button[aria-label="Show password"]').should('exist')
    
    // Testa se o botão de limpar email tem aria-label
    cy.get('input[type="email"]').type('test@example.com')
    cy.get('span[aria-label="Limpar email"]').should('exist')
  })
})
