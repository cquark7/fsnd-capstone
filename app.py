import datetime

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from auth.auth import AuthError, requires_auth
from models import setup_db, Author, Book


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS,PATCH'
        )
        return response

    @app.route('/')
    def main():
        message = '''
        <div style="background-color:lightblue; text-align:center">
            <h3>FSND Capstone Project: Biblio</h3>
            <p>by Deepankar Sharma</p>
        </div> '''
        return message

    @app.route('/authors')
    @requires_auth('get:authors')
    def get_authors(payload):
        selection = Author.query.all()
        authors = []
        for author in selection:
            authors.append(author.format())
        return jsonify({
            'status': True,
            'authors': authors
        })

    @app.route('/books')
    @requires_auth('get:books')
    def get_books(payload):
        selection = Book.query.all()

        books = []

        for book in selection:
            books.append(book.format())

        return jsonify({
            'status': True,
            'books': books
        })

    @app.route('/authors/<id>', methods=['DELETE'])
    @requires_auth('delete:authors')
    def delete_author(payload, id):
        selection = Author.query.get(id)

        if not selection:
            abort(404)

        try:
            selection.delete()
        except Exception as e:
            print('it could not be deleted', e)

        return jsonify({
            'status': True,
            'author': id
        })

    @app.route('/books/<id>', methods=['DELETE'])
    @requires_auth('delete:books')
    def book(payload, id):
        selection_id = Book.query.get(id)

        if not selection_id:
            abort(404)

        try:
            selection = Book.query.filter(Book.title == selection_id.title).all()
            for book in selection:
                book.delete()
        except Exception as e:
            print('it could not be deleted', e)

        return jsonify({
            'status': True,
            'book': selection_id.title
        })

    @app.route('/authors/add', methods=['POST'])
    @requires_auth('post:authors')
    def post_author(payload):
        res = request.get_json()

        if not res:
            abort(400)

        try:
            author = Author(
                name=res['name'],
                age=res['age'],
                gender=res['gender']
            )
            author.insert()

        except Exception as e:
            print('Object creation failed!', e)
            abort(500)
        return jsonify({
            'status': True,
            'author': [author.format()]
        })

    @app.route('/books/add', methods=['POST'])
    @requires_auth('post:books')
    def post_books(payload):
        res = request.get_json()

        books = []
        if not res:
            abort(400)
        try:
            index = 0
            for _ in res['author_id']:
                book = Book(
                    title=res['title'],
                    publishDate=datetime.datetime.strptime(res['publishDate'], '%a, %d %b %Y %H:%M:%S %Z'),
                    author_id=res['author_id'][index]
                )
                books.append(book.format())
                book.insert()
                index += 1

        except Exception as e:
            print('we couldnt create the object. Reason :', e)
            abort(500)

        return jsonify({
            'status': True,
            'book': books
        })

    @app.route('/authors/<id>', methods=['PATCH'])
    @requires_auth('patch:authors')
    def patch_authors(payload, id):
        res = request.get_json()

        if not res:
            abort(404)

        author = Author.query.get(id)

        try:
            if 'name' in res:
                author.name = res['name']
            if 'age' in res:
                author.age = res['age']
            if 'gender' in res:
                author.gender = res['gender']

            author.update()

        except Exception as e:
            print('we couldnt create the object. Reason :', e)
            abort(500)

        return jsonify({
            'status': True,
            'author': [author.format()]
        })

    @app.route('/books/<id>', methods=['PATCH'])
    @requires_auth('patch:books')
    def patch_books(payload, id):
        res = request.get_json()

        if not res:
            abort(404)

        book = Book.query.get(id)

        try:
            if 'title' in res:
                book.title = res['title']
            if 'publishDate' in res:
                book.publishDate = res['publishDate']
            if 'author_id' in res:
                book.author_id = res['author_id']

            book.update()

        except Exception as e:
            print('Object creation failer:', e)
            abort(500)

        return jsonify({
            'status': True,
            'book': [book.format()]
        })

    # Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Request"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The server can not find the requested resource."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed."
        }), 405

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "You are not authorized!"
        }), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
