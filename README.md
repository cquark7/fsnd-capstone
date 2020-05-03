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
/authors|GET|Returns all authors as a List|`curl https://deepankar-fsnd-capstone.herokuapp.com//authors -H"Authorization: Bearer <Token>"`|`{"authors": [{"age": 42, "gender": "male", "id": 7, "name": "plato"}, {"age": 31, "gender": "male", "id": 9, "name": "descartes"},], "status": true}`|
/books|GET|Returns all the books as a List|`curl https://deepankar-fsnd-capstone.herokuapp.com//books -H"Authorization: Bearer <Token>"`|`{"books": [{      "author_id": 4, "id": 13, "release date": "Fri, 21 Aug 2015 00:00:00 GMT", "title": "book_title" }, {"author_id": 1, "id": 8, "release date": "Thu, 29 Fev 2020 00:00:00 GMT", "title": interstellar" }],"status": true }`|
/authors/<id>|PATCH|Modify information about a author. Returns the modified author as a list|`curl https://deepankar-fsnd-capstone.herokuapp.com//authors/2 -X PATCH -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"name":"plato", "age":"42"}'`|`{"author": [{"age": 42, "gender": "male", "id": 2, "name": "plato"}], status": true}`|
/books/<id>|PATCH|Modify information about a book. Returns the modified author as a list|`curl https://deepankar-fsnd-capstone.herokuapp.com//books/5 -X PATCH -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"title":"interstellar","publishDate":"Fri, 21 Aug 2015 00:00:00 GMT"}'`|`{"book": [{"author_id": 1, "id": 5, "release date": "Thu, 29 Fev 2020 00:00:00 GMT", "title": "interstellar"}], "status": true}`|
/authors/<id>|DELETE|Delete the specified author by ID.|`curl https://deepankar-fsnd-capstone.herokuapp.com//authors/3 -X DELETE -H"Authorization: Bearer <Token>"`|`{"author": "3", "status": true}`|
/books/<id>|DELETE|Delete the specified book by ID.|`curl https://deepankar-fsnd-capstone.herokuapp.com//books/1 -X DELETE -H"Authorization: Bearer <Token>"`|`{"book": "Stephen Hawking", "status": true}`|
/authors/add|POST|Adds a new author to the database. Returns the author as a List|`curl https://deepankar-fsnd-capstone.herokuapp.com//authors/add -X POST -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"name":"descartes", "age":"31","gender":"male"}'`|`{ "author": [{"age": 31, "gender": "male", "id": 1, "name": "descartes" }], "status": true }`|
/books/add|POST|Adds a new book to the database. Returns the book as a List. If more than one author is specified on the authors List one identical book will be created for each author.|`curl -X POST https://deepankar-fsnd-capstone.herokuapp.com//books/add  -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"title":"book_title","publishDate":"Fri, 21 Aug 2015 00:00:00 GMT","author_id": ["1","2","4"]}'`|`{ "book": [{"author_id": "1", "id": null, "release date": "Fri, 21 Aug 2015 00:00:00 GMT", "title": "book_title" }, { "author_id": "2", "id": null, "release date": "Fri, 21 Aug 2015 00:00:00 GMT", "title": "book_title" },{"author_id": "4", "id": null, "release date": "Fri, 21 Aug 2015 00:00:00 GMT", "title": book_title"}], "status": true}`|


## Tokens

#### Bibliophile
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZlTU50Q1VNZ0lFN2FTTENYcEhQdiJ9.eyJpc3MiOiJodHRwczovL2RlZXBhbmthci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhZWViOTQ2YjY5YmMwYzEyZjAzZDc2IiwiYXVkIjoiYmlibGlvIiwiaWF0IjoxNTg4NTIyODk5LCJleHAiOjE1ODg2MDkyOTksImF6cCI6IkVYektLR2JxallxMXFVTk5RSkxCc25oaFNqWmwwWEVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyJdfQ.P3vtEeXcY_XXajt4FukzEag-EI0PLEXq3XXwHDwxRiZQTGj6gH080-C1aBR3-WTTsrExat7YL6IjQexJQPKHM3ET9-serzWzRShuM0ytSNEUH1EcTvdSxM9b_P5qbMziukPC9JjCsO9VCJRnzHF37oDA5UuQnE0zrpnIIzieUg_6ce8iX-MpR9tpCEeTl-XDtu2qbQ0HQYz4yzt_LbS7qWsQjiokcIMg-RFmFoeILCWMpdjxNOisFUWN9U287x4V1BE1G3BBlOuynsUZceOvNYS6-PI0fiJENPHBhMp9YlhaCrQbs7C6CdvSsN3U55DD_18KM0Ou3hqpUnTmdCjtEQ`

#### Author
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZlTU50Q1VNZ0lFN2FTTENYcEhQdiJ9.eyJpc3MiOiJodHRwczovL2RlZXBhbmthci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhZWViZTg2YjY5YmMwYzEyZjAzZTNhIiwiYXVkIjoiYmlibGlvIiwiaWF0IjoxNTg4NTI4MDM0LCJleHAiOjE1ODg2MTQ0MzQsImF6cCI6IkVYektLR2JxallxMXFVTk5RSkxCc25oaFNqWmwwWEVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIl19.eAgn3t628V1xb1nLR6q-TrSbKYBkw24snJhMwSUxncGDNtEvhHf0xuat2D9wsSgG9hx12biPF63oL61G46WkJP4TCoFkcwGqDyeZCedkF9eM-39QUMAyquH3iWL0QP1nKzqnNb7Hk71R7Dn41cFk921dPda_DOoq6CYmfp43wnPXnfk-ogAx-NwFWpFoDo2iO_BVbKtVmjCi0fOA3UbHwQ-RgnydULjxnRfyNArSCNSqjpIDALKpUEEFS9XgdGi_La-UQqmEtkznYINB5B4os2jp_Sbvwl-nZ_oYToX2h7OybNF0fRAP_unkIg7nWQ-1c6tJm-zfRARxxT76sPweCA`

#### Publisher
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZlTU50Q1VNZ0lFN2FTTENYcEhQdiJ9.eyJpc3MiOiJodHRwczovL2RlZXBhbmthci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhZWVjMWIxY2MxYWMwYzE0ODBiNDNhIiwiYXVkIjoiYmlibGlvIiwiaWF0IjoxNTg4NTI4MTExLCJleHAiOjE1ODg2MTQ1MTEsImF6cCI6IkVYektLR2JxallxMXFVTk5RSkxCc25oaFNqWmwwWEVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImRlbGV0ZTpib29rcyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIiwicG9zdDpib29rcyJdfQ.XjGDtCCs7BaSlUBo7xvRHoERVDrW6BcV-kVwEvi0gQh0u59pz0tkDBI20HWkn_AnTF7jOkrdsakzs1MypU-vL3eheYqpqBeZYDifdHUsnfibacnsA-kEwi2fB8nlpDHqTqDk7_D-I2CqvaVUtD3oUPoJtcYDg6Pm7MZ9ItpzHyowH6pYWwQjodTrCLSsoZ4q_zuV13BROrDtWHGUn97tjH85HW-Gn259actP9-ulIQMxsl8o_FJwFj-MqsrjV6bfjA3KVWSS5Z4j6VhGSYqb-MRw9jEpTqPkooI662yx3-jRhsFTL448tsDiUZicMS2fQZ3liztyZVviN3gT6MSenQ`


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
