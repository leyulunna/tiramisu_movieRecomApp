# models.py

from . import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    year = db.Column(db.String(4))
    imdb_id = db.Column(db.String(20))
    # poster = db.Column(db.String(255))

    def __init__(self, title, year, imdb_id, poster):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.poster = poster

class Favorite(db.Model):
    imdb_id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(4))
    
    def __init__(self, imdb_id, title, year):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id