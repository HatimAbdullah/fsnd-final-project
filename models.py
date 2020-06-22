import os
from sqlalchemy import Column, String, Integer, create_engine, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "alphadb"
database_path = "postgres://{}:{}@{}/{}".format('postgres','1234','localhost:5433', database_name)

db = SQLAlchemy()
Base = declarative_base()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

actor_movie = Table('actor_movie', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('actor_id', Integer, ForeignKey('Actor.id')),
    Column('movie_id', Integer, ForeignKey('Movie.id'))
)
#class actor_movie(db.Model):
   # __tablename__ = 'actor_movie'
   # id = db.Column(db.Integer, primary_key=True)
   # actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
   # movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
  #  actor = relationship(Actor, backref=backref("actor_movie", cascade="all, delete-orphan"))
 #   movie = relationship(movie, backref=backref("actor_movie", cascade="all, delete-orphan"))

class Actor(db.Model):
    __tablename__ = 'Actor'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    movies = relationship("Movie", secondary=actor_movie)

    def __init__(self, name, gender, age, movies):
        self.name = name
        self.gender = gender
        self.age = age
        self.movies = movies

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'movies': self.movies
        }


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    release_date = Column(String)
    actors = relationship("Actor", secondary=actor_movie)

    def __init__(self, name, release_date, actors):
        self.name = name
        self.release_date = release_date
        self.actors = actors

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'name': self.name,
            'release_date': self.release_date,
            'actors': self.actors
        }

