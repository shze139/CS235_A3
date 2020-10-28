from datetime import datetime

from app.models.user import User
from app.models.genre import Genre
from app.models.director import Director
from app.models.actor import Actor
from app.models.movie import Movie
from app.models.review import Review
from app.models.watchlist import WatchList



import pytest

@pytest.fixture()
def user():
    return User('jack', '123456')

@pytest.fixture()
def genre():
    return Genre('Action')

@pytest.fixture()
def director():
    return Director('James Gunn')

@pytest.fixture()
def actor():
    return Actor('Chris Pratt')

@pytest.fixture()
def movie(genre, director, actor):
    rank = 1
    title = 'Guardians of the Galaxy'
    genres = [genre]
    description = 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'
    directors = [director]
    actors = [actor]
    year = 2014
    runtime = 121
    rating = 8.1
    votes = 757074
    revenue = 333.13
    metascore = 76
    return Movie(rank, title, genres, description, directors, actors, year, runtime, rating, votes, revenue, metascore)

@pytest.fixture()
def review(user, movie):
    content = 'first review'
    timestamp = datetime(year=2020,month=9,day=9)
    return Review(content, timestamp, user, movie)

@pytest.fixture()
def watchlist(user, movie):
    return WatchList(user, movie)


def test_user(user):
    assert user.username == 'jack'
    assert user.password == '123456'

    for movie in user.watchList:
        assert False

def test_genre(genre):
    assert genre.name == 'Action'

def test_director(director):
    assert director.full_name == 'James Gunn'

def test_actor(actor):
    assert actor.full_name == 'Chris Pratt'

def test_movie(movie, genre, actor, director):
    assert movie.rank == 1
    assert movie.title == 'Guardians of the Galaxy'

    assert len(movie.actors) == 1
    assert len(movie.genre) == 1
    assert len(movie.director) == 1

    assert actor in movie.actors
    assert genre in movie.genre
    assert director in movie.director

def test_review(review, user, movie):
    assert review.content == 'first review'
    assert review.timestamp == '2020-09-09 00:00:00'
    assert review.user == user
    assert review.movie == movie

def test_watchlist(watchlist, user, movie):
    assert watchlist.user == user
    assert watchlist.movie == movie




