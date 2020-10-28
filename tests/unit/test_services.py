import pytest
from datetime import datetime
import app.auth.services as auth_services
import app.movie.services as movie_services

def test_login_failed(repo):
    username = 'jack'
    password = '123456'

    with pytest.raises(auth_services.LoginFailedException):
        auth_services.login(username, password, repo)

def test_register_success(repo):
    username = 'jack'
    password = '123456'

    auth_services.register(username, password, repo)

    auth_services.login(username, password, repo)

def test_register_username_exists(repo):
    username1 = 'jack'
    password1 = '123456'
    auth_services.register(username1, password1, repo)

    username2 = 'jack'
    password2 = '123456'
    with pytest.raises(auth_services.UsernameNotUniqueException):
        auth_services.register(username2, password2, repo)

def test_movie_detail(repo):
    movieId = 1
    movieTitle = 'Guardians of the Galaxy'
    movie = movie_services.get_movie(movieId, repo)

    assert movie.id == movieId
    assert movie.title == movieTitle

def test_movie_not_found(repo):
    movieId = 9999

    with pytest.raises(movie_services.MovieNotFoundException):
        movie_services.get_movie(movieId, repo)

def test_add_to_watchlist(repo):
    username = 'jack'
    password = '123456'
    auth_services.register(username, password, repo)

    movieId = 1

    movie_services.add_to_watchlist(username, movieId, repo)

    user = auth_services.login(username, password, repo)
    movie = movie_services.get_movie(movieId, repo)

    assert movie in user.watchList
    assert len(user.watchList) == 1

def test_add_to_watchlist_user_not_found(repo):
    username = 'jack'
    movieId = 1

    with pytest.raises(movie_services.UserNotFoundException):
        movie_services.add_to_watchlist(username, movieId, repo)


def test_add_to_watchlist_movie_not_found(repo):
    username = 'jack'
    password = '123456'
    auth_services.register(username, password, repo)

    movieId = 9999

    with pytest.raises(movie_services.MovieNotFoundException):
        movie_services.add_to_watchlist(username, movieId, repo)

def test_remove_from_watchlist(repo):
    username = 'jack'
    password = '123456'
    auth_services.register(username, password, repo)
    user = auth_services.login(username, password, repo)

    movieId = 1
    movie_services.add_to_watchlist(username, movieId, repo)

    assert len(user.watchList) == 1

    movie_services.remove_from_watchlist(username, movieId, repo)
    assert len(user.watchList) == 0

def test_add_review(repo):
    username = 'jack'
    password = '123456'
    auth_services.register(username, password, repo)

    movieId = 1
    content = 'first review'
    movie_services.add_review(content, username, movieId, repo)

    movie = movie_services.get_movie(movieId, repo)

    assert len(movie.reviews) == 1
    assert movie.reviews[0].content == content
