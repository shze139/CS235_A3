from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, Float, Text,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from ..models.movie import Movie
from ..models.actor import Actor
from ..models.genre import Genre
from ..models.director import Director
from ..models.user import User
from ..models.review import Review
from ..models.watchlist import WatchList

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), unique=True, nullable=False)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), unique=True, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('rank', Integer),
    Column('title', String(255)),
    Column('description', Text),
    Column('year', Integer),
    Column('runtime', Float),
    Column('rating', Float),
    Column('votes', Integer),
    Column('revenue', Float),
    Column('metascore', Float),
    Column('poster', String(255), nullable=True)
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

movie_directors = Table(
    'movie_directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('director_id', Integer, ForeignKey('directors.id'))
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('content', Text, nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

watchlist = Table(
    'watchlist', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('movie_id', Integer, ForeignKey('movies.id'))
)

def map_model_to_tables():
    mapper(Movie, movies, properties={
        '_id': movies.c.id,
        '_rank': movies.c.rank,
        '_title': movies.c.title,
        '_genre': relationship(Genre, secondary=movie_genres),
        '_description': movies.c.description,
        '_director': relationship(Director, secondary=movie_directors),
        '_actors': relationship(Actor, secondary=movie_actors),
        '_year': movies.c.year,
        '_runtime': movies.c.runtime,
        '_rating': movies.c.rating,
        '_votes': movies.c.votes,
        '_revenue': movies.c.revenue,
        '_metascore': movies.c.metascore,
        '_poster': movies.c.poster,
        '_reviews': relationship(Review)
    })

    mapper(Actor, actors, properties={
        '_id': actors.c.id,
        '_full_name': actors.c.full_name
    })

    mapper(Genre, genres, properties={
        '_id': genres.c.id,
        '_name': genres.c.name
    })

    mapper(Director, directors, properties={
        '_id': directors.c.id,
        '_full_name': directors.c.full_name
    })

    mapper(User, users, properties={
        '_id': users.c.id,
        '_username': users.c.username,
        '_password': users.c.password,
        '_watchList': relationship(Movie, secondary=watchlist)
    })

    mapper(Review, reviews, properties={
        '_id': reviews.c.id,
        '_content': reviews.c.content,
        '_timestamp': reviews.c.timestamp,
        '_user': relationship(User),
        '_movie': relationship(Movie),
    })

    mapper(WatchList, watchlist, properties={
        '_id': watchlist.c.id,
        '_user': relationship(User),
        '_movie': relationship(Movie),
    })
