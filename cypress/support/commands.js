// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

import Chance from "chance"
const chance = new Chance()

const getIframeDocument = () => {
  return cy
  .get('.cke_wysiwyg_frame')
  // Cypress yields jQuery element, which has the real
  // DOM element under property "0".
  // From the real DOM iframe element we can get
  // the "document" element, it is stored in "contentDocument" property
  // Cypress "its" command can access deep properties using dot notation
  // https://on.cypress.io/its
  .its('0.contentDocument').should('exist')
}

const getIframeBody = () => {
  // get the document
  return getIframeDocument()
  // automatically retries until body is loaded
  .its('body').should('not.be.undefined')
  // wraps "body" DOM element to allow
  // chaining more Cypress commands, like ".find(...)"
  .then(cy.wrap)
}

Cypress.Commands.add('sign-up', (username, pass) => {
  cy.visit('http://127.0.0.1')
  cy.log('Logging in')
  cy.get('.alt-login').click()
  cy.url().should('contain', 'login')
  cy.contains('Sign Up').click()
  cy.get("input[name='username']").type(username)
  cy.get("input[name='password1']").type(pass)
  cy.get("input[name='password2']").type(pass)
  cy.get("button[type='submit']").click()
})

Cypress.Commands.add('login', (username, pass) => {
  cy.visit('http://127.0.0.1')
  cy.log('Logging in')
  cy.get('.alt-login').click()
  cy.url().should('contain', 'login')
  cy.get("input[name='login']").type(username)
  cy.get("input[name='password']").type(pass)
  cy.get("button[type='submit']").click()
})

Cypress.Commands.add('selectTemplate', (templateName) => {
  cy.contains('New Mailing').click()
  cy.get('select').select('default')
  cy.get(`a[href='/new/${templateName}']`).click()
})

Cypress.Commands.add('fillOutSubjectGroup', (i) => {
  cy.get(`input[name="subjects-${i-1}-subject"]`).type(chance.string({alpha:true}))
  cy.get(`input[name="subjects-${i-1}-preview_text"]`).type(chance.string({alpha:true}))
})

Cypress.Commands.add('addSubjectGroup', () => {
  cy.get('#add_subjects').click()
  cy.get('input[name="subjects-1-subject"]').should('be.visible')
})

Cypress.Commands.add('fillOutFromLine', () => {
  cy.get(`input[name="from_line"]`)
    .type(`${chance.string({alpha:true, length:5})} <${chance.email()}>`)
})

Cypress.Commands.add('fillOutReplyTo', () => {
  cy.get(`input[name="reply_to"]`)
    .type(`${chance.string({alpha:true, length:5})} <${chance.email()}>`)
})

Cypress.Commands.add('addBodyContent', () => {
  getIframeBody().type(chance.string({length:100}))
})

Cypress.Commands.add('selectTagType', (tagType) => {
  cy.get(`li[data-tagtype="${tagType}"]`).click()
  cy.get('#tag-modal-search').click()
  cy.get('#ui-id-1').should('be.visible')
});

Cypress.Commands.add('addSomeTags', () => {
  cy.get('#openTagModal').click()
  cy.get('.tag_modal').should('be.visible')
  cy.selectTagType('OWN')
  cy.contains('Amanda').click()
  cy.selectTagType('HELP')
  cy.contains('Angel').click()
  //consider creating an object with these values
  cy.get('#saveCloseModal').click()
})

Cypress.Commands.add('addMailingNotes', () => {
  cy.get('textarea[name="notes"]').type(chance.string({alpha:true}))
})

Cypress.Commands.add('saveMailing', () => {
  cy.get('#mailing-form').click()
  cy.contains('GMAIL')
})

Cypress.Commands.add('selectAnExistingMailing', () => {
  cy.contains('Existing Mailing').click()
  cy.get('.exist-mailing--title').first().click()
})

Cypress.Commands.add('reviewLitmusPreviews', () => {
  cy.contains('GMAIL').click()
  cy.get('#preview-GMAIL').should('be.visible')
  cy.contains('IPAD').click()
  cy.get('#preview-IPAD').should('be.visible')
  cy.contains('ANDROID').click()
  cy.get('#preview-ANDROID').should('be.visible')
  cy.contains('OUTLOOK').click()
  cy.get('#preview-OUTLOOK').should('be.visible')
})


Cypress.Commands.add('removeSubjectGroup', () => {
  cy.get('input[name="subjects-1-subject"]').should('be.visible')
  cy.get('#delete_subjects').click()
  expect(document.querySelector('input[name="subjects-1-subject"]')).to.be.null
})

Cypress.Commands.add('updateBodyContent', () => {
  cy.addBodyContent()
})

Cypress.Commands.add('addSomeMoreTags', () => {
  cy.get('#openTagModal').click()
  cy.get('.tag_modal').should('be.visible')
  cy.selectTagType('OWN')
  cy.contains('Morgan').click()
  cy.selectTagType('HELP')
  cy.get('.ui-menu-item-wrapper').contains('Amanda').click()
  //consider creating an object with these values
  cy.get('#saveCloseModal').click()
})

Cypress.Commands.add('changeTemplates', (templateName) => {
  cy.get('select[name="template"]').select(templateName)
})


Cypress.Commands.add('selectUnapprovedMailing', () => {
  cy.contains('Approvals').click()
  cy.get('.exist-mailing--title').first().click()
})

Cypress.Commands.add('approveMailing', () => {
  cy.get('#id_approved').click()
  cy.saveMailing()
  cy.contains('Existing').click()
  cy.get('.exist-mailing--title').first().click()
  cy.get('#save-ak-mailer').should('be.visible')
})