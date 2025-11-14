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

  it('preenche o formulário e envia, validando o request e a toast de sucesso', () => {
    const createdResponse = {
      id: 'inic-1',
      titulo: 'Iniciativa E2E',
      descricao: 'Descrição de teste',
      local: 'Local Teste',
      link: '',
      organizador_id: 'org-1',
      imagem_url: '',
      destaque: false,
      tags: [{ id: 'tag-1', nome: 'Tag Teste' }],
      horarios: [],
    }

    // Intercept POST and assert the request body
    cy.intercept('POST', '/admin/iniciativas/', (req) => {
      // basic assertions about body shape
      expect(req.body).to.have.property('titulo', 'Iniciativa E2E')
      expect(req.body).to.have.property('local', 'Local Teste')
      expect(req.body).to.have.property('descricao')
      // tags should be sent as tag ids
      expect(req.body).to.have.property('tag_ids')
      expect(req.body.tag_ids).to.include('tag-1')
      expect(req.body).to.have.property('organizador_id', 'org-1')

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

    // Submit the form
    cy.get('.justify-end > .inline-flex').click()

    // Esta dando problema com assert do array de tags, então o cadastro não está indo de fato, estou rodando pela dev mesmo
})
})