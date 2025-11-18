/// <reference types="cypress" />

describe('Criar Iniciativa test', () => {
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

  it.only('preenche o formulário e envia, validando o request e a toast de sucesso', () => {
    const createdResponse = {
      titulo: 'Iniciativa E2E',
      descricao: 'Descrição de teste',
      local: 'Local Teste',
      link: 'https://exemplo.com',
      imagem_url: '',
      destaque: false,
      horarios: [],
    }

    // Intercept POST and assert the request body
    cy.intercept('POST', '/admin/iniciativas/', (req) => {
      // basic assertions about body shape
      expect(req.body).to.have.property('titulo', 'Iniciativa E2E')
      expect(req.body).to.have.property('local', 'Local Teste')
      expect(req.body).to.have.property('descricao', 'Descrição de teste')
      expect(req.body).to.have.property('link', 'https://exemplo.com')

      req.reply({ statusCode: 201, body: createdResponse })
    }).as('postIniciativa')

    // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')

    cy.get('.rounded-md').contains('Nova iniciativa').click()

    // Fill out the form
    cy.get('input[name="titulo"]').type('Iniciativa E2E')
    cy.get('input[name="local"]').type('Local Teste')
    cy.get('textarea[name="descricao"]').type('Descrição de teste')

    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('{enter}') // Fecha o dropdown de tags


    //  Tags
    cy.get('.grid > :nth-child(1) > .w-4').click() // Seleciona a primeira tag
    cy.get('.grid > :nth-child(3) > .w-4').click() // Desseleciona a primeira tag

    cy.get(':nth-child(3) > .text-card-foreground').click()

    cy.get('[name="link"]').type('https://exemplo.com')


    // Ambos botões de adicionar horario e adicionar descrição não estou conseguindo pegar o path correto

    // Botão de adicionar descrição extra
    cy.get('button[id="descricaoExtraButton"]').click()
    cy.get('[name="descricoes_extras.0"]').type('teste')

    // Botão de adicionar horario
    cy.get('button[id="addScheduleButton"]').click()
    
    // Escolher dia
    cy.get('.space-y-4 > :nth-child(1) > .flex > div > .inline-flex').click()
    cy.get('.bg-accent > .items-center').click()

    // Horarios de inicio e fim
    cy.get('.space-y-4 > :nth-child(2) > .flex-col').type('{enter}') 
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{downArrow} {enter}')

    // Submit the form
    cy.get('.justify-end > .inline-flex').click()
})

  it('simula erro 409 quando iniciativa já existe', () => {
    // perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get('.rounded-md').contains('Nova iniciativa').click()

    // stub API to return 409 Conflict
    cy.intercept('POST', '/admin/iniciativas/', {
      statusCode: 409,
      body: { detail: 'Já existe uma iniciativa com este título.' },
    }).as('postIniciativaConflict')

    // Fill out the form with data that would conflict
    cy.get('input[name="titulo"]').type('Iniciativa E2E')
    cy.get('input[name="local"]').type('Local Teste')
    cy.get('textarea[name="descricao"]').type('Descrição de teste')
    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('{enter}') // Fecha o dropdown de organizador

    //  Tags
    cy.get('.grid > :nth-child(1) > .w-4').click() // Seleciona a primeira tag
    cy.get('.grid > :nth-child(3) > .w-4').click() // Desseleciona a primeira tag

    cy.get(':nth-child(3) > .text-card-foreground').click()

    cy.get('[name="link"]').type('https://exemplo.com')

    cy.get('.justify-end > .inline-flex').click()

    cy.wait('@postIniciativaConflict').then(({ response }) => {
      expect(response.statusCode).to.equal(409)
      expect(response.body).to.have.property('detail', 'Já existe uma iniciativa com este título.')
    })
  })

  it('simula erro 500 do servidor ao criar iniciativa', () => {
    // perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')
    cy.get('.rounded-md').contains('Nova iniciativa').click()

    // stub API to return 500 Internal Server Error
    cy.intercept('POST', '/admin/iniciativas/', {
      statusCode: 500,
      body: { detail: 'Erro interno do servidor' },
    }).as('postIniciativaServerError')

    // Fill out the form
    cy.get('input[name="titulo"]').type('Iniciativa E2E')
    cy.get('input[name="local"]').type('Local Teste')
    cy.get('textarea[name="descricao"]').type('Descrição de teste')
    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('{enter}') // Fecha o dropdown de organizador

    //  Tags
    cy.get('.grid > :nth-child(1) > .w-4').click() // Seleciona a primeira tag
    cy.get('.grid > :nth-child(3) > .w-4').click() // Desseleciona a primeira tag

    cy.get(':nth-child(3) > .text-card-foreground').click()

    cy.get('[name="link"]').type('https://exemplo.com')

    cy.get('.justify-end > .inline-flex').click()

    cy.wait('@postIniciativaServerError').then(({ response }) => {
      expect(response.statusCode).to.equal(500)
      expect(response.body).to.have.property('detail', 'Erro interno do servidor')
    })
  })
    it('faltando titulo', () => {

    // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')

    cy.get('.rounded-md').contains('Nova iniciativa').click()

    // Fill out the form
    cy.get('input[name="local"]').type('Local Teste')
    cy.get('textarea[name="descricao"]').type('Descrição de teste')

    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('{enter}') // Fecha o dropdown de tags


    //  Tags
    cy.get('.grid > :nth-child(1) > .w-4').click() // Seleciona a primeira tag
    cy.get('.grid > :nth-child(3) > .w-4').click() // Desseleciona a primeira tag

    cy.get(':nth-child(3) > .text-card-foreground').click()

    cy.get('[name="link"]').type('https://exemplo.com')

    // Ambos botões de adicionar horario e adicionar descrição não estou conseguindo pegar o path correto

    // Botão de adicionar descrição extra
    //cy.get(':nth-child(2) > .@container/card-header > .flex-col > .gap-2').click()
    //cy.get('[name="descricoes_extras.0"]').type('teste')

    // Botão de adicionar horario
    //cy.get(':nth-child(3) > .bg-white > .\@container\/card-header > .justify-between > .flex-col > .gap-2').click()
    
    // Escolher dia
    //cy.get('.space-y-4 > :nth-child(1) > .flex > div > .inline-flex').click()
    //cy.get('.bg-accent > .items-center').click()

    // Horarios de inicio e fim
    //cy.get('.space-y-4 > :nth-child(2) > .flex-col').type('{enter}') 
    //cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{enter}') 


    cy.get('.justify-end > .inline-flex').click()

    // validation message for nome
    cy.get('.leading-tight').should('contain.text', 'O título deve ter pelo menos 3 caracteres.')
  })

  it('faltando local', () => {
    
    // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')

    cy.get('.rounded-md').contains('Nova iniciativa').click()

    // Fill out the form
    cy.get('input[name="titulo"]').type('Iniciativa E2E')
    cy.get('textarea[name="descricao"]').type('Descrição de teste')

    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('p{enter}') // Fecha o dropdown de tags


    //  Tags
    cy.get('.grid > :nth-child(1) > .w-4').click() // Seleciona a primeira tag
    cy.get('.grid > :nth-child(3) > .w-4').click() // Desseleciona a primeira tag

    cy.get(':nth-child(3) > .text-card-foreground').click()

    cy.get('[name="link"]').type('https://exemplo.com')

    // Ambos botões de adicionar horario e adicionar descrição não estou conseguindo pegar o path correto

    // Botão de adicionar descrição extra
    //cy.get(':nth-child(2) > .@container/card-header > .flex-col > .gap-2').click()
    //cy.get('[name="descricoes_extras.0"]').type('teste')

    // Botão de adicionar horario
    //cy.get(':nth-child(3) > .bg-white > .\@container\/card-header > .justify-between > .flex-col > .gap-2').click()
    
    // Escolher dia
    //cy.get('.space-y-4 > :nth-child(1) > .flex > div > .inline-flex').click()
    //cy.get('.bg-accent > .items-center').click()

    // Horarios de inicio e fim
    //cy.get('.space-y-4 > :nth-child(2) > .flex-col').type('{enter}') 
    //cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{enter}') 


    cy.get('.justify-end > .inline-flex').click()

    // validation message for nome
    cy.get('.leading-tight').should('contain.text', 'O local deve ter pelo menos 3 caracteres')
  })

  it('faltando tags', () => {
    // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')

    cy.get('.rounded-md').contains('Nova iniciativa').click()

    // Fill out the form
    cy.get('input[name="titulo"]').type('Iniciativa E2E')
    cy.get('input[name="local"]').type('Local Teste')
    cy.get('textarea[name="descricao"]').type('Descrição de teste')

    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('{enter}') 

    cy.get('[name="link"]').type('https://exemplo.com')

    // Ambos botões de adicionar horario e adicionar descrição não estou conseguindo pegar o path correto

    // Botão de adicionar descrição extra
    //cy.get(':nth-child(2) > .@container/card-header > .flex-col > .gap-2').click()
    //cy.get('[name="descricoes_extras.0"]').type('teste')

    // Botão de adicionar horario
    //cy.get(':nth-child(3) > .bg-white > .\@container\/card-header > .justify-between > .flex-col > .gap-2').click()
    
    // Escolher dia
    //cy.get('.space-y-4 > :nth-child(1) > .flex > div > .inline-flex').click()
    //cy.get('.bg-accent > .items-center').click()

    // Horarios de inicio e fim
    //cy.get('.space-y-4 > :nth-child(2) > .flex-col').type('{enter}') 
    //cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{enter}') 


    cy.get('.justify-end > .inline-flex').click()

    // validation message for nome
    cy.get('.leading-tight').should('contain.text', 'Adicione pelo menos uma tag.')
  })

  it('faltando descricao', () => {
    // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')

    cy.get('.rounded-md').contains('Nova iniciativa').click()

    // Fill out the form
    cy.get('input[name="titulo"]').type('Iniciativa E2E')
    cy.get('input[name="local"]').type('Local Teste')

    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('{enter}') // Fecha o dropdown de tags


    //  Tags
    cy.get('.grid > :nth-child(1) > .w-4').click() // Seleciona a primeira tag
    cy.get('.grid > :nth-child(3) > .w-4').click() // Desseleciona a primeira tag

    cy.get(':nth-child(3) > .text-card-foreground').click()

    cy.get('[name="link"]').type('https://exemplo.com')

    // Ambos botões de adicionar horario e adicionar descrição não estou conseguindo pegar o path correto

    // Botão de adicionar descrição extra
    //cy.get(':nth-child(2) > .@container/card-header > .flex-col > .gap-2').click()
    //cy.get('[name="descricoes_extras.0"]').type('teste')

    // Botão de adicionar horario
    //cy.get(':nth-child(3) > .bg-white > .\@container\/card-header > .justify-between > .flex-col > .gap-2').click()
    
    // Escolher dia
    //cy.get('.space-y-4 > :nth-child(1) > .flex > div > .inline-flex').click()
    //cy.get('.bg-accent > .items-center').click()

    // Horarios de inicio e fim
    //cy.get('.space-y-4 > :nth-child(2) > .flex-col').type('{enter}') 
    //cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{enter}') 


    cy.get('.justify-end > .inline-flex').click()

    // validation message for nome
    cy.get('.leading-tight').should('contain.text', 'A descrição deve ter pelo menos 10 caracteres.')
  })

  it('link de formato errado', () => {
    // First perform login
    cy.visit('/admin')
    cy.get('input[type="email"]').clear().type('admin@bah.com.br')
    cy.get('input[type="password"]').clear().type('admin123')
    cy.get('button[type="submit"]').click()

    cy.url().should('include', '/iniciativas')

    cy.get('.rounded-md').contains('Nova iniciativa').click()

    // Fill out the form
    cy.get('input[name="titulo"]').type('Iniciativa E2E')
    cy.get('input[name="local"]').type('Local Teste')
    cy.get('textarea[name="descricao"]').type('Descrição de teste')

    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('{enter}') // Fecha o dropdown de tags


    //  Tags
    cy.get('.grid > :nth-child(1) > .w-4').click() // Seleciona a primeira tag
    cy.get('.grid > :nth-child(3) > .w-4').click() // Desseleciona a primeira tag

    cy.get(':nth-child(3) > .text-card-foreground').click()

    cy.get('[name="link"]').type('teste.com')

    // Ambos botões de adicionar horario e adicionar descrição não estou conseguindo pegar o path correto

    // Botão de adicionar descrição extra
    //cy.get(':nth-child(2) > .@container/card-header > .flex-col > .gap-2').click()
    //cy.get('[name="descricoes_extras.0"]').type('teste')

    // Botão de adicionar horario
    //cy.get(':nth-child(3) > .bg-white > .\@container\/card-header > .justify-between > .flex-col > .gap-2').click()
    
    // Escolher dia
    //cy.get('.space-y-4 > :nth-child(1) > .flex > div > .inline-flex').click()
    //cy.get('.bg-accent > .items-center').click()

    // Horarios de inicio e fim
    //cy.get('.space-y-4 > :nth-child(2) > .flex-col').type('{enter}') 
    //cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{enter}') 


    cy.get('.justify-end > .inline-flex').click()

    // validation message for nome
    cy.get('.leading-tight').should('contain.text', 'O link deve ser uma URL válida.')
  })
})