# models.py

from . import db

class Movie(db.Model):
    __tablename__ = 'movies'
    imdb_id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(255))
    year = db.Column(db.String(4))

    def __init__(self, title, year, imdb_id):
        self.imdb_id = imdb_id
        self.title = title
        self.year = year

class Search(db.Model):
    __tablename__ = 'searches'
    imdb_id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(255))
    year = db.Column(db.String(4))

    def __init__(self, imdb_id, title, year):
        self.imdb_id = imdb_id
        self.title = title
        self.year = year
