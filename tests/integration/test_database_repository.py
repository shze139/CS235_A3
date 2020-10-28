from datetime import date, datetime

import pytest

from app.adapters.database_repository import SqlAlchemyRepository
from app.models.user import User
from app.models.genre import Genre
from app.models.director import Director
from app.models.actor import Actor
from app.models.movie import Movie
from app.models.review import Review
from app.models.watchlist import WatchList

def make_user():
    return User('jack', '123456')

def make_movie():
    rank = 1
    title = 'Guardians of the Galaxy'
    genres = [Genre('Action'), Genre('Adventure'), Genre('Sci-Fi')]
    description = 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'
    directors = [Director('James Gunn')]
    actors = [Actor('Chris Pratt'), Actor('Vin Diesel'), Actor('Bradley Cooper'), Actor('Zoe Saldana')]
    year = 2014
    runtime = 121
    rating = 8.1
    votes = 757074
    revenue = 333.13
    metascore = 76
    return Movie(rank, title, genres, description, directors, actors, year, runtime, rating, votes, revenue, metascore)

def test_add_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('jack', '123456')
    repo.add_user(user)

    user1 = repo.get_user(user.username)

    assert user == user1

def test_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    username = 'jack'
    password = '123456'
    user = User(username, password)
    repo.add_user(user)


    assert repo.get_user(username) == user

    username_not_exists = 'tom'
    assert repo.get_user(username_not_exists) is None

def test_get_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movieId1 = 1
    movieTitle1 = 'Guardians of the Galaxy'
    movieGenre1 = ['Action' , 'Adventure' , 'Sci-Fi']
    movieActors1 = ['Chris Pratt' , 'Vin Diesel' , 'Bradley Cooper' , 'Zoe Saldana']
    movieDirectors1 = ['James Gunn']

    movie1 = repo.get_movie(movieId1)
    assert movie1.title == movieTitle1
    assert [item.name for item in movie1.genre] == movieGenre1
    assert [item.full_name for item in movie1.actors] == movieActors1
    assert [item.full_name for item in movie1.director] == movieDirectors1

    movieId2 = 9999
    movie2 = repo.get_movie(movieId2)
    assert movie2 is None


def test_search_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    page = 1
    size = 50
    by = 'all'
    key = ''

    result = repo.search_movies(key, by, page, size)
    assert result.get('total') == 1000
    assert result.get('totalPage') == 20

    by = 'actor'
    key = 'test'
    result = repo.search_movies(key, by, page, size)
    assert result.get('total') == 0
    assert result.get('totalPage') == 0

    by = 'director'
    key = 'James Gunn'
    result = repo.search_movies(key, by, page, size)
    assert result.get('total') == 3
    assert result.get('totalPage') == 1

def test_add_and_remove_watch(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = make_user()

    movieId = 1
    movie = repo.get_movie(movieId)

    watchList = WatchList(user, movie)
    repo.add_watch(watchList)
    assert movie in user.watchList

    repo.remove_watch(user, movie)
    assert movie not in user.watchList

def test_add_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movieId = 1
    movie = repo.get_movie(movieId)

    user = make_user()
    repo.add_user(user)

    timestamp = datetime(2020, 10, 1)
    review = Review('first review', timestamp, user, movie)
    repo.add_review(review)

    assert len(movie.reviews) == 1
    assert review in movie.reviews

def test_poster(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movieId = 1
    movie = repo.get_movie(movieId)

    repo.get_poster(movie)

    assert movie.poster == 'https://m.media-amazon.com/images/M/MV5BMTAwMjU5OTgxNjZeQTJeQWpwZ15BbWU4MDUxNDYxODEx._V1_SX300.jpg'