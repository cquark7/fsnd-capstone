import datetime
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Author, Book

TOKEN_PUBLISHER = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZlTU50Q1VNZ0lFN2FTTENYcEhQdiJ9.eyJpc3MiOiJodHRwczovL2RlZXBhbmthci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhZWVjMWIxY2MxYWMwYzE0ODBiNDNhIiwiYXVkIjoiYmlibGlvIiwiaWF0IjoxNTg4NTI4MTExLCJleHAiOjE1ODg2MTQ1MTEsImF6cCI6IkVYektLR2JxallxMXFVTk5RSkxCc25oaFNqWmwwWEVZIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXV0aG9ycyIsImRlbGV0ZTpib29rcyIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9ycyIsInBhdGNoOmJvb2tzIiwicG9zdDphdXRob3JzIiwicG9zdDpib29rcyJdfQ.XjGDtCCs7BaSlUBo7xvRHoERVDrW6BcV-kVwEvi0gQh0u59pz0tkDBI20HWkn_AnTF7jOkrdsakzs1MypU-vL3eheYqpqBeZYDifdHUsnfibacnsA-kEwi2fB8nlpDHqTqDk7_D-I2CqvaVUtD3oUPoJtcYDg6Pm7MZ9ItpzHyowH6pYWwQjodTrCLSsoZ4q_zuV13BROrDtWHGUn97tjH85HW-Gn259actP9-ulIQMxsl8o_FJwFj-MqsrjV6bfjA3KVWSS5Z4j6VhGSYqb-MRw9jEpTqPkooI662yx3-jRhsFTL448tsDiUZicMS2fQZ3liztyZVviN3gT6MSenQ'


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

    def test_post_author(self):
        table_length = Author.query.all()

        res = self.client().post('/authors/add', headers={
            'Authorization': TOKEN_PUBLISHER},
                                 json=self.new_author
                                 )

        data = res.get_json()

        self.assertEqual(data['status'], True)
        self.assertGreater(len(Author.query.all()), len(table_length))

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

    def test_get_all_books(self):
        res = self.client().get('/books', headers={
            'Authorization': TOKEN_PUBLISHER})

        data = res.get_json()
        selection = Book.query.all()
        self.maxDiff = None
        self.assertEqual(data['status'], True)
        self.assertEqual(data['books'], [book.format() for book in selection])

    def test_post_book(self):
        table_length = Book.query.all()
        res = self.client().post('/books/add', headers={
            'Authorization': TOKEN_PUBLISHER},
                                 json=self.new_book)

        data = res.get_json()

        self.assertEqual(data['status'], True)
        self.assertGreater(len(Book.query.all()), len(table_length))

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


# Execute tests!
if __name__ == "__main__":
    unittest.main()
