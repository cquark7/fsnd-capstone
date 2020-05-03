import datetime
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Author, Book

TOKEN_PUBLISHER = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZlTU50Q1VNZ0lFN2FTTENYcEhQdiJ9.eyJpc3MiOiJodHRwczovL2RlZXBhbmthci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhZWVjMWIxY2MxYWMwYzE0ODBiNDNhIiwiYXVkIjoiYmlibGlvIiwiaWF0IjoxNTg4NTI4MTExLCJleHAiOjE1ODg2MTQ1MTEsImF6cCI6IkVYektLR2JxallxMXFVTk5RSkxCc25oaFNqWmwwWEVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImRlbGV0ZTpib29rcyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIiwicG9zdDpib29rcyJdfQ.XjGDtCCs7BaSlUBo7xvRHoERVDrW6BcV-kVwEvi0gQh0u59pz0tkDBI20HWkn_AnTF7jOkrdsakzs1MypU-vL3eheYqpqBeZYDifdHUsnfibacnsA-kEwi2fB8nlpDHqTqDk7_D-I2CqvaVUtD3oUPoJtcYDg6Pm7MZ9ItpzHyowH6pYWwQjodTrCLSsoZ4q_zuV13BROrDtWHGUn97tjH85HW-Gn259actP9-ulIQMxsl8o_FJwFj-MqsrjV6bfjA3KVWSS5Z4j6VhGSYqb-MRw9jEpTqPkooI662yx3-jRhsFTL448tsDiUZicMS2fQZ3liztyZVviN3gT6MSenQ'
TOKEN_AUTHOR = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZlTU50Q1VNZ0lFN2FTTENYcEhQdiJ9.eyJpc3MiOiJodHRwczovL2RlZXBhbmthci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhZWViZTg2YjY5YmMwYzEyZjAzZTNhIiwiYXVkIjoiYmlibGlvIiwiaWF0IjoxNTg4NTI4MDM0LCJleHAiOjE1ODg2MTQ0MzQsImF6cCI6IkVYektLR2JxallxMXFVTk5RSkxCc25oaFNqWmwwWEVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIl19.eAgn3t628V1xb1nLR6q-TrSbKYBkw24snJhMwSUxncGDNtEvhHf0xuat2D9wsSgG9hx12biPF63oL61G46WkJP4TCoFkcwGqDyeZCedkF9eM-39QUMAyquH3iWL0QP1nKzqnNb7Hk71R7Dn41cFk921dPda_DOoq6CYmfp43wnPXnfk-ogAx-NwFWpFoDo2iO_BVbKtVmjCi0fOA3UbHwQ-RgnydULjxnRfyNArSCNSqjpIDALKpUEEFS9XgdGi_La-UQqmEtkznYINB5B4os2jp_Sbvwl-nZ_oYToX2h7OybNF0fRAP_unkIg7nWQ-1c6tJm-zfRARxxT76sPweCA'
TOKEN_BIBLIOPHILE = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZlTU50Q1VNZ0lFN2FTTENYcEhQdiJ9.eyJpc3MiOiJodHRwczovL2RlZXBhbmthci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhZWViOTQ2YjY5YmMwYzEyZjAzZDc2IiwiYXVkIjoiYmlibGlvIiwiaWF0IjoxNTg4NTIyODk5LCJleHAiOjE1ODg2MDkyOTksImF6cCI6IkVYektLR2JxallxMXFVTk5RSkxCc25oaFNqWmwwWEVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXV0aG9ycyIsImdldDpib29rcyJdfQ.P3vtEeXcY_XXajt4FukzEag-EI0PLEXq3XXwHDwxRiZQTGj6gH080-C1aBR3-WTTsrExat7YL6IjQexJQPKHM3ET9-serzWzRShuM0ytSNEUH1EcTvdSxM9b_P5qbMziukPC9JjCsO9VCJRnzHF37oDA5UuQnE0zrpnIIzieUg_6ce8iX-MpR9tpCEeTl-XDtu2qbQ0HQYz4yzt_LbS7qWsQjiokcIMg-RFmFoeILCWMpdjxNOisFUWN9U287x4V1BE1G3BBlOuynsUZceOvNYS6-PI0fiJENPHBhMp9YlhaCrQbs7C6CdvSsN3U55DD_18KM0Ou3hqpUnTmdCjtEQ'


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.new_author = {
            'name': 'Stephen Hawking',
            'age': 42,
            'gender': 'male',
        }

        self.new_book = {
            'author_id': '11',
            'publishDate': datetime.datetime(2022, 2, 22),
            'title': 'Gladiator',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        selection = Book.query.filter(Book.title == 'Gladiator').all()
        for book in selection:
            book.delete()
        selection = Author.query.filter(Author.name == 'Stephen Hawking').all()
        for author in selection:
            author.delete()
        pass

    def test_get_all_authors(self):
        res = self.client().get('/authors', headers={
            'Authorization': TOKEN_PUBLISHER}
                                )
        data = res.get_json()
        selection = Author.query.all()

        self.assertEqual(data['status'], True)
        self.assertEqual(data['authors'], [author.format() for author in selection])

    def test_get_all_authors_error(self):
        res = self.client().get('/authors', headers={})
        data = res.get_json()
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)

    def test_post_author(self):
        table_length = Author.query.all()

        res = self.client().post('/authors/add', headers={
            'Authorization': TOKEN_PUBLISHER},
                                 json=self.new_author
                                 )

        data = res.get_json()

        self.assertEqual(data['status'], True)
        self.assertGreater(len(Author.query.all()), len(table_length))

    def test_post_author_error(self):
        new_author = self.new_author.copy()
        del new_author['name']
        res = self.client().post('/authors/add', headers={
            'Authorization': TOKEN_PUBLISHER},
                                 json=new_author
                                 )
        data = res.get_json()
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_patch_author(self):
        author = Author(
            name='Hello',
            age=22,
            gender='male'
        )
        author.id = 371
        author.insert()

        res = self.client().patch('/authors/371', headers={
            'Authorization': TOKEN_PUBLISHER},
                                  json={
                                      "name": "Plato",
                                      "age": "67"
                                  }
                                  )
        data = res.get_json()

        author = Author.query.filter(Author.id == 371).one_or_none()

        self.assertEqual(data['status'], True)
        self.assertEqual(author.name, 'Plato')

        author.delete()

    def test_patch_author_error(self):
        author = Author(
            name='Hello',
            age=22,
            gender='male'
        )
        author.id = 451
        author.insert()

        res = self.client().patch('/authors/451', headers={
            'Authorization': TOKEN_PUBLISHER}, json={"name": None})
        data = res.get_json()
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        author.delete()

    def test_delete_author(self):
        author = Author(
            name='Brian Greene',
            age=55,
            gender='male'
        )
        author.id = 333
        author.insert()

        res = self.client().delete('/authors/333', headers={
            'Authorization': TOKEN_PUBLISHER},
                                   )

        data = res.get_json()
        selection = Author.query.filter(Author.id == 333).one_or_none()

        self.assertEqual(data['status'], True)
        self.assertEqual(selection, None)

    def test_delete_author_error(self):
        res = self.client().delete('/authors/452', headers={
            'Authorization': TOKEN_PUBLISHER},
                                   )
        data = res.get_json()
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_get_all_books(self):
        res = self.client().get('/books', headers={
            'Authorization': TOKEN_PUBLISHER})

        data = res.get_json()
        selection = Book.query.all()
        self.maxDiff = None
        self.assertEqual(data['status'], True)
        self.assertEqual(data['books'], [book.format() for book in selection])

    def test_get_all_books_error(self):
        res = self.client().get('/books', headers={})
        data = res.get_json()
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)

    def test_post_book(self):
        table_length = Book.query.all()
        res = self.client().post('/books/add', headers={
            'Authorization': TOKEN_PUBLISHER},
                                 json=self.new_book)

        data = res.get_json()

        self.assertEqual(data['status'], True)
        self.assertGreater(len(Book.query.all()), len(table_length))

    def test_post_book_error(self):
        new_book = self.new_book.copy()
        del new_book['author_id']
        res = self.client().post('/books/add', headers={
            'Authorization': TOKEN_PUBLISHER},
                                 json=new_book
                                 )
        data = res.get_json()
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_patch_book(self):
        book = Book(
            title='Sapiens',
            publishDate=datetime.datetime(2022, 2, 22),
            author_id='11'
        )
        book.id = 249
        book.insert()

        res = self.client().patch('/books/249', headers={
            'Authorization': TOKEN_PUBLISHER},
                                  json={
                                      "title": "Gene",
                                      "publishDate": "2021-03-25 11:55:11.271041"
                                  }
                                  )

        data = res.get_json()
        selection = Book.query.filter(Book.id == 249).one_or_none()

        self.assertEqual(data['status'], True)
        self.assertEqual(selection.title, 'Gene')

        selection.delete()

    def test_patch_book_error(self):
        # Book ID doesn't exist
        res = self.client().patch('/books/256', headers={
            'Authorization': TOKEN_PUBLISHER}, json={"title": "Gene",
                                                     "publishDate": "2021-03-25 11:55:11.271041"
                                                     })
        data = res.get_json()
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_delete_book(self):
        book = Book(
            title='new_book',
            publishDate=datetime.datetime(2022, 2, 22),
            author_id='11'
        )
        book.id = 144
        book.insert()

        res = self.client().delete('/books/144', headers={
            'Authorization': TOKEN_PUBLISHER},
                                   )

        data = res.get_json()
        selection = Book.query.filter(Book.id == 144).one_or_none()
        self.assertEqual(data['status'], True)
        self.assertEqual(selection, None)

    def test_delete_book_error(self):
        res = self.client().delete('/books/460', headers={
            'Authorization': TOKEN_PUBLISHER},
                                   )
        data = res.get_json()
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    # RBAC tests start from here.
    # RBAC tests of Publisher Role are already included in the above tests.
    def test_bibliophile_get_success(self):
        res = self.client().get('/books', headers={
            'Authorization': TOKEN_BIBLIOPHILE})

        data = res.get_json()
        selection = Book.query.all()
        self.maxDiff = None
        self.assertEqual(data['status'], True)
        self.assertEqual(data['books'], [book.format() for book in selection])

    def test_bibliophile_post_failure(self):
        res = self.client().post('/books/add', headers={
            'Authorization': TOKEN_BIBLIOPHILE},
                                 json=self.new_book)

        self.assertEqual(res.status_code, 401)

    def test_author_post_author_success(self):
        res = self.client().post('/authors/add', headers={
            'Authorization': TOKEN_AUTHOR},
                                 json=self.new_author
                                 )
        data = res.get_json()
        self.assertEqual(data['status'], True)

    def test_author_post_book_failure(self):
        res = self.client().post('/books/add', headers={
            'Authorization': TOKEN_AUTHOR},
                                 json=self.new_book)
        self.assertEqual(res.status_code, 401)


# Execute tests!
if __name__ == "__main__":
    unittest.main()
