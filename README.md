## Ticket 1
_Show your name, surname, bio, contacts on the main page._

Create basic django-project that would present your name, surname, date of birth, bio, contacts on the main page. 

Data should be stored in the DB, that's:
- manage.py syncdb
- manage.py runserver
- open the browser and all data are in, loaded from fixtures

Use pip requirements and virtualenv to manage your third party packages dependencies.

Use south, you'll need it later.

There should be Makefile with test target running your tests (make test to verify it).

Mockup: http://framebox.org/Awq-bCzXsh

## Ticket 3
_Create middleware that stores all http requests in the DB._

Also, on a separate page show last 10 http requests that are stored by middleware.

This page should update asynchronously as new requests come in, updating page header as well.

If there are N new requests, page title should start with (N).

As page is viewed by user, all requests should be considered as read and the title should return to the initial state.

Mockup: http://framebox.org/Awv-QVXKyN

## Ticket 5
_Create page with a form that allows to edit data, presented on the main page._

Create page with a form that allows to edit data, presented on the main page.

Use own  django widget.

Make this form ajax, using jquery.forms

- submit form via ajax
- indicate loading state
- disable form during submit, so nothing could be entered/changed there

Just JSON should be transmitted between the frontend and the backend.

Add auth to this page.

Upload and show photo. 

Photo should be scaled on the backend to 200x200, maintaining aspect ratio.

Mockups:

- http://framebox.org/wSk-YPMrdM
- http://framebox.org/AMzD-BTbGcL
 
## Ticket 8
 _Template tag, django command, signal processor_

Create tag that accepts any object and renders the link to its admin edit page.

Create tag that accepts any object and renders the link to its admin edit page ({% edit_link request.user %})

Mockup: http://framebox.org/AMZF-FNEhjy

---

Create django command that prints all project models and the count of objects in every model.
Also:
- duplicate output to STDERR, prefixing each line with "error: "
- write bash script which execute your command and save output of stderr into file. File name should be current date with extension .dat

---
 
Create signal processor that, for every model, creates the db entry about the object creation/editing/deletion

## Ticket 13
_Your customer sends the change request. Task: understand what he needs and implement._

Customer's text:

_About requests log: we have to add a priortiy field, 
so we can show the different requests in the order we want. 
Priority 1 (or = 0) will be the standard selection._

Task: understand what he needs and implement.

42-test template
===========================

A Django 1.6+ project template

Use fortytwo_test_task.settings when deploying with getbarista.com

### Recomendations
* apps in apps/ folder
* use per-app templates folders
* use per-app static folders
* use migrations
* use settings.local for different environments
* common templates live in templates/
* common static lives in assets/
* management commands should be proxied to single word make commands, e.g make test

