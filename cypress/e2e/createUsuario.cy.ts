/// <reference types="cypress" />

describe('Criar Usuario test', () => {
  beforeEach(() => {
    // Visita a página de login antes de cada teste
    cy.visit('/admin')

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
      cy.url().should('include', '/iniciativas')
    })
  })
  })
  it('Cadastra usuario com sucesso', () => {
    

    // Intercept POST and respond with 201 Created
    cy.intercept('POST', '/admin/usuarios/', (req) => {
      req.reply({
        statusCode: 201,
        body: { id: 'mock-id', detail: 'Usuário criado com sucesso' },
      })
    }).as('postUsuario')

    // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get(':nth-child(4) > .block > .group').click()

    cy.contains('Novo usuário').click()

    // Fill out the form
    cy.get('input[name="nome"]').type('Teste')
    cy.get('input[name="sobrenome"]').type('da Silva')
    cy.get('input[name="email"]').type('teste@example.com')
    cy.get('input[name="senha"]').type('senha123')

    cy.get('.inline-flex').contains('Salvar Usuário').click()
    // ensure the mocked request was triggered and returned 201
    cy.wait('@postUsuario').then(({ response }) => {
      expect(response.statusCode).to.equal(201)
      expect(response.body).to.have.property('detail', 'Usuário criado com sucesso')
    })
    })

  // Additional API error cases (do not modify existing tests above)
  it('simula erro 409 quando email já cadastrado', () => {
    // perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get(':nth-child(4) > .block > .group').click()
    cy.contains('Novo usuário').click()

    // stub API to return 409 Conflict
    cy.intercept('POST', '/admin/usuarios/', {
      statusCode: 409,
      body: { detail: 'Email já cadastrado' },
    }).as('postUsuarioConflict')

    // Fill out the form
    cy.get('input[name="nome"]').type('Teste')
    cy.get('input[name="sobrenome"]').type('da Silva')
    cy.get('input[name="email"]').type('teste@example.com')
    cy.get('input[name="senha"]').type('senha123')

    cy.get('.inline-flex').contains('Salvar Usuário').click()

    cy.wait('@postUsuarioConflict').then(({ response }) => {
      expect(response.statusCode).to.equal(409)
      expect(response.body).to.have.property('detail', 'Email já cadastrado')
    })
  })

  it('simula erro 500 do servidor ao criar usuário', () => {
    // perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get(':nth-child(4) > .block > .group').click()
    cy.contains('Novo usuário').click()

    // stub API to return 500 Internal Server Error
    cy.intercept('POST', '/admin/usuarios/', {
      statusCode: 500,
      body: { detail: 'Erro interno do servidor' },
    }).as('postUsuarioServerError')

    // Fill out the form
    cy.get('input[name="nome"]').type('Teste')
    cy.get('input[name="sobrenome"]').type('da Silva')
    cy.get('input[name="email"]').type('teste@example.com')
    cy.get('input[name="senha"]').type('senha123')

    cy.get('.inline-flex').contains('Salvar Usuário').click()

    cy.wait('@postUsuarioServerError').then(({ response }) => {
      expect(response.statusCode).to.equal(500)
      expect(response.body).to.have.property('detail', 'Erro interno do servidor')
    })
  })
    it('teste com email faltante', () => {
         // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get(':nth-child(4) > .block > .group').click()

    cy.contains('Novo usuário').click()

    // Fill out the form
    cy.get('input[name="nome"]').type('Teste')
    cy.get('input[name="sobrenome"]').type('da Silva')
    cy.get('input[name="senha"]').type('senha123')

    cy.get('.inline-flex').contains('Salvar Usuário').click()

    // validation message for email
    cy.get('.leading-tight').should('contain.text', 'O email deve ser válido')
    })
    it('teste com nome faltante', () => {
         // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get(':nth-child(4) > .block > .group').click()

    cy.contains('Novo usuário').click()

    // Fill out the form
    cy.get('input[name="sobrenome"]').type('da Silva')
    cy.get('input[name="email"]').type('teste@example.com')
    cy.get('input[name="senha"]').type('senha123')

    cy.get('.inline-flex').contains('Salvar Usuário').click()

    // validation message for nome
    cy.get('.leading-tight').should('contain.text', 'O nome deve ter pelo menos 3 caracteres')
    })
    it('teste com sobrenome faltante', () => {
         // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get(':nth-child(4) > .block > .group').click()

    cy.contains('Novo usuário').click()

    // Fill out the form
    cy.get('input[name="nome"]').type('Teste')
    cy.get('input[name="email"]').type('teste@example.com')
    cy.get('input[name="senha"]').type('senha123')

    cy.get('.inline-flex').contains('Salvar Usuário').click()

    // validation message for sobrenome
    cy.get('.leading-tight').should('contain.text', 'O sobrenome deve ter pelo menos 3 caracteres')
    })
    it('teste com senha curta', () => {
         // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get(':nth-child(4) > .block > .group').click()

    cy.contains('Novo usuário').click()

    // Fill out the form
    cy.get('input[name="nome"]').type('Teste')
    cy.get('input[name="sobrenome"]').type('da Silva')
    cy.get('input[name="email"]').type('teste@example.com')
    cy.get('input[name="senha"]').type('12345')

    cy.get('.inline-flex').contains('Salvar Usuário').click()
    
    // validation message for senha
    cy.get('.leading-tight').should('contain.text', 'A senha deve ter pelo menos 6 caracteres')
    })
})