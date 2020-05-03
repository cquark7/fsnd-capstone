import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()


# Binds flask app and SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


# Reset DB
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


# Authors Table
class Author(db.Model):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    book = relationship("Book", back_populates="author")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        """ Inserts a new model into a database. """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ Updates a new model into a database. """
        db.session.commit()

    def delete(self):
        """ Deletes a new model into a database. """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """ Formatted representation of the author model. """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }


# Books Table
class Book(db.Model):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    publishDate = Column(DateTime(timezone=False), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", back_populates="book")

    def __init__(self, title, publishDate, author_id):
        self.title = title
        self.publishDate = publishDate
        self.author_id = author_id

    def insert(self):
        """ Inserts a new model into a database """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """ Updates a new model into a database. """
        db.session.commit()

    def delete(self):
        """ Deletes a new model into a database. """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """ Formatted representation of the author model. """
        return {
            'author_id': self.author_id,
            'id': self.id,
            'release date': self.publishDate.strftime('%c'),
            'title': self.title,
        }
