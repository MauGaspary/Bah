/// <reference types="cypress" />

// ***********************************************
// Custom commands for BAH Frontend tests
// ***********************************************

// Custom command to login with credentials
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/admin')
  cy.get('input[type="email"]').type(email)
  cy.get('input[type="password"]').type(password)
  cy.get('button[type="submit"]').click()
})

// Custom command to clear localStorage
Cypress.Commands.add('clearAuth', () => {
  cy.window().then((win) => {
    win.localStorage.removeItem('access_token')
  })
})

// Custom command to set auth token in localStorage
Cypress.Commands.add('setAuthToken', (token: string) => {
  cy.window().then((win) => {
    win.localStorage.setItem('access_token', token)
  })
})

// Custom command to check if user is authenticated
Cypress.Commands.add('isAuthenticated', () => {
  cy.window().then((win) => {
    const token = win.localStorage.getItem('access_token')
    return cy.wrap(!!token)
  })
})

// Extend Cypress chainable interface
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>
      clearAuth(): Chainable<void>
      setAuthToken(token: string): Chainable<void>
      isAuthenticated(): Chainable<boolean>
    }
  }
}