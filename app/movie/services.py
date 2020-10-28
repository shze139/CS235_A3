from datetime import datetime

from app.models.review import Review
from app.models.watchlist import WatchList

class MovieNotFoundException(Exception):
    pass

class UserNotFoundException(Exception):
    pass


def get_movie(movieId, repo):
    movie = repo.get_movie(movieId)
    if movie is None:
        raise MovieNotFoundException

    if movie.poster is None:
        repo.get_poster(movie)

    return movie

def has_watch(movie, username, repo):
    if username:
        user = repo.get_user(username)
        if user and movie in user.watchList:
            return True
    return False

def add_review(content, username, movieId, repo):
    user = repo.get_user(username)
    if user is None:
        raise UserNotFoundException

    movie = repo.get_movie(movieId)
    if movie is None:
        raise MovieNotFoundException

    timestamp = datetime.now()
    repo.add_review(Review(content, timestamp, user, movie))

def add_to_watchlist(username, movieId, repo):
    user = repo.get_user(username)
    if user is None:
        raise UserNotFoundException

    movie = repo.get_movie(movieId)
    if movie is None:
        raise MovieNotFoundException

    repo.add_watch(WatchList(user, movie))

def remove_from_watchlist(username, movieId, repo):
    user = repo.get_user(username)
    if user is None:
        raise UserNotFoundException

    movie = repo.get_movie(movieId)
    if movie is None:
        raise MovieNotFoundException

    repo.remove_watch(user, movie)

