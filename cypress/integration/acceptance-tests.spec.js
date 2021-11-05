/// <reference types="cypress" />

import fixture from "../fixtures/example.json"

describe('Walkthrough', () => {
  beforeEach(() => {
    cy.viewport('macbook-13')
    cy.login(fixture.username, fixture.password)
  })

  it('can create a new mailing', () => {
    cy.selectTemplate('petition-one')
    cy.fillOutSubjectGroup(1)
    cy.addSubjectGroup()
    cy.fillOutSubjectGroup(2)
    cy.fillOutFromLine()
    cy.fillOutReplyTo()
    cy.addBodyContent()
    cy.addSomeTags()
    cy.addMailingNotes()
    cy.changeTemplates('updated-default')
    cy.saveMailing()
  });

  it('can edit and save an existing mailing', () => {
    cy.selectAnExistingMailing()
    cy.reviewLitmusPreviews()
    cy.removeSubjectGroup()
    cy.updateBodyContent()
    cy.addSomeMoreTags()
    cy.changeTemplates('petition-one')
    cy.reviewLitmusPreviews()
  })

  it('can approve existing mailing', () => {
    cy.selectUnapprovedMailing()
  //   cy.checkAllFieldsFilledOut()
  //   cy.checkAllTagsFilledOut()
    cy.reviewLitmusPreviews()
    cy.approveMailing()
  })
})