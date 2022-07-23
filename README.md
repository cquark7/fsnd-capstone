## Introduction: Biblio
I created the backend of a book service called 'Biblio'.

## Installation
- Download the latest version of Python 3 from the official website.
- Create a virtual environment to run the project.
- Install dependencies:
```shell
pip3 install -r requirements.txt
```

## Setting up the database

- Create a new database in postgres:
```shell
createdb capstone
```

- To restore the database:
```
psql capstone < db_dump.sql
```

## Start the Flask server
- Set env variables
```sh
sourse setup.sh
```
- Run flask server locally:
```shell
flask run --reload
```
Note: Set `DATABASE_URL` and `TEST_DATABASE_URL` environment variable before starting the server.

## Testing
To run the tests, run:
```
dropdb capstone_test && createdb capstone_test
psql capstone_test < db_dump.sql
python test_app.py
```

## Heroku live server:
- Base URL `https://deepankar-fsnd-capstone.herokuapp.com/`


## API Endpoints
URI|Method|Action|Curl example|return example
---|---|---|---|---
/|GET|test the application is running|`curl https://deepankar-fsnd-capstone.herokuapp.com/`|'FSND Capstone Project: Biblio'
/authors|GET|Returns all authors as a List|`curl https://deepankar-fsnd-capstone.herokuapp.com/authors -H"Authorization: Bearer <Token>"`|`{"authors": [{"age": 42, "gender": "male", "id": 7, "name": "plato"}, {"age": 31, "gender": "male", "id": 9, "name": "descartes"},], "status": true}`|
/books|GET|Returns all the books as a List|`curl https://deepankar-fsnd-capstone.herokuapp.com/books -H"Authorization: Bearer <Token>"`|`{"books": [{      "author_id": 4, "id": 13, "release date": "Fri, 21 Aug 2015 00:00:00 GMT", "title": "book_title" }, {"author_id": 1, "id": 8, "release date": "Thu, 29 Fev 2020 00:00:00 GMT", "title": interstellar" }],"status": true }`|
/authors/`<id>`|PATCH|Modify information about a author. Returns the modified author as a list|`curl https://deepankar-fsnd-capstone.herokuapp.com/authors/2 -X PATCH -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"name":"plato", "age":"42"}'`|`{"author": [{"age": 42, "gender": "male", "id": 2, "name": "plato"}], status": true}`|
/books/`<id>`|PATCH|Modify information about a book. Returns the modified author as a list|`curl https://deepankar-fsnd-capstone.herokuapp.com/books/5 -X PATCH -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"title":"interstellar","publishDate":"Fri, 21 Aug 2015 00:00:00 GMT"}'`|`{"book": [{"author_id": 1, "id": 5, "release date": "Thu, 29 Fev 2020 00:00:00 GMT", "title": "interstellar"}], "status": true}`|
/authors/`<id>`|DELETE|Delete the specified author by ID.|`curl https://deepankar-fsnd-capstone.herokuapp.com/authors/3 -X DELETE -H"Authorization: Bearer <Token>"`|`{"author": "3", "status": true}`|
/books/`<id>`|DELETE|Delete the specified book by ID.|`curl https://deepankar-fsnd-capstone.herokuapp.com/books/1 -X DELETE -H"Authorization: Bearer <Token>"`|`{"book": "Stephen Hawking", "status": true}`|
/authors/add|POST|Adds a new author to the database. Returns the author as a List|`curl https://deepankar-fsnd-capstone.herokuapp.com/authors/add -X POST -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"name":"descartes", "age":"31","gender":"male"}'`|`{ "author": [{"age": 31, "gender": "male", "id": 1, "name": "descartes" }], "status": true }`|
/books/add|POST|Adds a new book to the database. Returns the book as a List. If more than one author is specified on the authors List one identical book will be created for each author.|`curl -X POST https://deepankar-fsnd-capstone.herokuapp.com/books/add  -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"title":"book_title","publishDate":"Fri, 21 Aug 2015 00:00:00 GMT","author_id": ["1","2","4"]}'`|`{ "book": [{"author_id": "1", "id": null, "release date": "Fri, 21 Aug 2015 00:00:00 GMT", "title": "book_title" }, { "author_id": "2", "id": null, "release date": "Fri, 21 Aug 2015 00:00:00 GMT", "title": "book_title" },{"author_id": "4", "id": null, "release date": "Fri, 21 Aug 2015 00:00:00 GMT", "title": book_title"}], "status": true}`|


## Permissions

Permissions|Details
---|---
get:books|Gets access to all books
get:authors|Gets access to all authors
post:authors|Can add authors to the DB
post:books|Can add books to the DB
delete:authors|Can delete authors from the DB
delete:books|Can delete books from the DB
patch:authors|Can modify authors from the DB
patch:books|Can modify books from the DB

## Roles

Role|Permissions
---|---
Bibliophile | get:books get:authors
Author | get:books get:authors post:authors delete:authors  patch:authors patch:books
Publisher | get:books get:authors post:authors post:books delete:authors delete:books patch:authors patch:books
