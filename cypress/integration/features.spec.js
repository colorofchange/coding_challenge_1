/// <reference types="cypress" />
import fixture from "../fixtures/example.json"

describe('Feature tests', ()=> {
  beforeEach(() => {
    cy.viewport('macbook-13')
    cy.login(fixture.username, fixture.password)
  })

  // it('errors on an empty form', () =>{
  //   cy.selectTemplate('petition-one')
  //   cy.saveMailing()
  // })

  it('handles tagging additions', () => {
    cy.selectAnExistingMailing()
    cy.addSomeTags()
    cy.addSomeMoreTags()
  })
})