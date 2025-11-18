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

  it('cadastra, validando o request e após exclui', () => {
    cy.intercept('DELETE', '**/iniciativas/*').as('deleteInitiativa');

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
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{downArrow}placeholder{enter}')

    // Submit the form
    cy.get('.justify-end > .inline-flex').click()

    // Validate the request and success toast
    cy.get('body').should('contain.text', 'Iniciativa criada com sucesso!')

    //  Deleting iniciativa
    cy.contains('.justify-between', 'Iniciativa E2E')     // acha o card pelo nome
    .parent()                                           // sobe um nível até o container correto
    .find('button')                                     // pega os botões dentro desse card
    .contains('Excluir')                                // acha o botão Excluir
    .click();

    cy.get('.text-xl').parent().find('button').contains('Excluir').click();

    cy.wait('@deleteInitiativa').then((intercept) => {
      expect(intercept.response.statusCode).to.eq(204); // ou 204 dependendo da API
    });
})

  it('cadastra inicitiva destaque, validando o request e após exclui', () => {
    cy.intercept('DELETE', '**/iniciativas/*').as('deleteInitiativa');

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

    //  Destaque
    cy.get('.peer').click()

    //  Organizador
    cy.get('[data-slot="card-content"] > :nth-child(1) > :nth-child(2) > .flex-col > div > .flex').click()
    cy.get('body').type('{enter}') // Fecha o dropdown de tags


    //  Tags
    cy.get('.grid > :nth-child(1) > .w-4').click() // Seleciona a primeira tag
    cy.get('.grid > :nth-child(3) > .w-4').click() // Desseleciona a primeira tag

    cy.get(':nth-child(3) > .text-card-foreground').click()

    cy.get('[name="link"]').type('https://exemplo.com')

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
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{downArrow}placeholder{enter}')

    // Submit the form
    cy.get('.justify-end > .inline-flex').click()

    // Validate the request and success toast
    cy.get('body').should('contain.text', 'Iniciativa criada com sucesso!')

    //  Deleting iniciativa
    cy.contains('.justify-between', 'Iniciativa E2E')     // acha o card pelo nome
    .parent()                                           // sobe um nível até o container correto
    .find('button')                                     // pega os botões dentro desse card
    .contains('Excluir')                                // acha o botão Excluir
    .click();

    cy.get('.text-xl').parent().find('button').contains('Excluir').click();

    cy.wait('@deleteInitiativa').then((intercept) => {
      expect(intercept.response.statusCode).to.eq(204); // ou 204 dependendo da API
    });
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
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{downArrow}placeholder{enter}')

    cy.get('.justify-end > .inline-flex').click()

    // validation message for titulo
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
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{downArrow}placeholder{enter}')

    cy.get('.justify-end > .inline-flex').click()

    // validation message for local
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
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{downArrow}placeholder{enter}')

    cy.get('.justify-end > .inline-flex').click()

    // validation message for tags
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
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{downArrow}placeholder{enter}')

    cy.get('.justify-end > .inline-flex').click()

    // validation message for descricao
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
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{downArrow}placeholder{enter}')

    cy.get('.justify-end > .inline-flex').click()

    // validation message for link
    cy.get('.leading-tight').should('contain.text', 'O link deve ser uma URL válida.')
  })

  it('horario invalido', () => {
    
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
    cy.get('.space-y-4 > :nth-child(3) > .flex-col').type('{enter}')

    cy.get('.justify-end > .inline-flex').click()

    // validation message for titulo
    cy.get('body').should('contain.text', 'Erro ao criar iniciativa')
  
  })
})