
from datetime import datetime
from app.models.user import User
from app.models.genre import Genre
from app.models.director import Director
from app.models.actor import Actor
from app.models.movie import Movie
from app.models.review import Review

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

def test_insert_user(empty_session):
    username = 'jack'
    password = '123456'
    user = User(username, password)
    empty_session.add(user)
    empty_session.commit()

    result = empty_session.execute('''
        select username, password from users where username = :username and password = :password
    ''', dict(username=username, password=password)).fetchone()

    assert result == (username, password)

def test_select_users(empty_session):
    user1 = User('jack', '123456')
    user2 = User('tom', '123456')

    empty_session.add(user1)
    empty_session.add(user2)
    empty_session.commit()

    result = empty_session.query(User).all()
    assert result == [user1, user2]

def test_genre(empty_session):
    genre1 = Genre('Action')
    genre2 = Genre('Adventure')

    empty_session.add(genre1)
    empty_session.add(genre2)
    empty_session.commit()

    result = empty_session.query(Genre).all()
    assert result == [genre1, genre2]

def test_actor(empty_session):
    actor1 = Actor('Ben Affleck')
    actor2 = Actor('Henry Cavill')

    empty_session.add(actor1)
    empty_session.add(actor2)
    empty_session.commit()

    result = empty_session.query(Actor).all()
    assert result == [actor1, actor2]

def test_director(empty_session):
    director1 = Director('Joss Whedon')
    director2 = Director('Zack Snyder')

    empty_session.add(director1)
    empty_session.add(director2)
    empty_session.commit()

    result = empty_session.query(Director).all()
    assert result == [director1, director2]

def test_movie(empty_session):
    movie = make_movie()

    empty_session.add(movie)
    empty_session.commit()

    movie1 = empty_session.query(Movie).filter(Movie._id == movie.id).first()
    assert movie == movie1
    assert movie.genre == movie1.genre
    assert movie.actors == movie1.actors
    assert movie.director == movie1.director

def test_review(empty_session):
    movie = make_movie()
    empty_session.add(movie)
    empty_session.commit()

    user = User('jack', '123456')
    empty_session.add(user)
    empty_session.commit()

    review_date = datetime(year=2020, month=10, day=10)
    review = Review('first review', review_date, user, movie)
    empty_session.add(review)
    empty_session.commit()

    assert review in movie.reviews

    result = empty_session.execute('select user_id, movie_id from reviews where id = :id', {'id':review.id}).fetchone()
    assert result[0] == user.id
    assert result[1] == movie.id


def test_watchlist(empty_session):
    movie = make_movie()

    empty_session.add(movie)
    empty_session.commit()

    user = User('jack', '123456')
    empty_session.add(user)
    empty_session.commit()


    user.watchList.append(movie)
    empty_session.merge(user)
    empty_session.commit()

    result = empty_session.execute('select movie_id from watchlist where user_id = :user_id', {'user_id': user.id}).fetchone()

    assert result[0] == movie.id
