## COC Engineering challenge

Thank you for your interest in Color of Change!

This challenge is a modified version of an repository we're actively working on and developing.

The Django app allows users to create `mailing` objects (All the components of an email like the subject, email body, sender address, and some other metadata such as tags and creator notes) and then send it to another system which handles actually sending out the email.

You can find a description of the mailing object and all the fields it contains in tempalates_app/models.py:80.

For this challenge you have 3 tasks:

- TODO: Get all mailing objects from the database and create a Paginator (This interview challenge should preload the DB with 12 mailing objects). You can do this in layout/views.py:71.
- Display all of the mailing objects in templates/layout/pages/select-mailing.html:38
  - Display must show date, subject and any associated tags of the mailing object
  - Feel free to style this in anyway you want. Flex your creativity!
- The `/select-mailing` page (http://127.0.0.1/select-mailing) has a small graphical bug from a previous PR, splitting the layout into 3 different columns. It should only be 2. Can you fix it? See `screenshot.png` in the root folder. The red arrows point out the extra column.
  - Our SCSS assets are in `static/scss`

The [Django Documentation](https://docs.djangoproject.com/en/3.0/) should have instructions on how to access objects from the database and other elements such as a Paginator and how HTML tempaltes work.

### Build instructions

- We build this project using Docker. You'll need to download and install it from [here](https://www.docker.com/products/docker-desktop):
  - Please reach out to us if you can't run Docker on your computer, or run into installation issues with Docker.
  - Clone this repository
  - With docker installed, navigate to the cloned repository and run this command : `docker-compose up --build`
    - Depending on your OS, you may need to (separately install docker-compose)[https://docs.docker.com/compose/install/]. (Mac OS and Windows shouldn't require this step)
  -