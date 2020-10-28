import csv
import os

from sqlalchemy.orm import scoped_session, contains_eager
from sqlalchemy.sql import text,select
from flask import _app_ctx_stack

from ..models.movie import Movie
from ..models.genre import Genre
from ..models.director import Director
from ..models.actor import Actor
from ..models.user import User
from ..models.watchlist import WatchList
from ..models.review import Review

import requests

import math

# from covid.domain.model import User, Article, Comment, Tag
from .repository import AbstractRepository
#
# tags = None
#
#
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()
#
#
class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = self._session_cm.session.query(User).filter(User._username == username).first()
        return user

    def get_movie(self, id):
        movie = self._session_cm.session.query(Movie).filter(Movie._id == id).first()
        return movie

    def search_movies(self, key:str, by:str, page:int = 1, size:int = 50):
        search = '%{}%'.format(key.strip())
        q = None
        if by == 'all':
            q1 = self._session_cm.session.query(Movie).filter(Movie._title.like(search))
            q = q1
        if by == 'actor' or by == 'all':
            sql = text('''
                                select distinct movie_actors.movie_id from movie_actors
                                left join actors on actors.id = movie_actors.actor_id
                                where actors.full_name like "{}"
                            '''.format(search))
            q2 = self._session_cm.session.query(Movie).filter(Movie._id.in_(select([text('movie_id')]).select_from(sql.columns())))
            if q:
                q = q.union(q2)
            else:
                q = q2
        if by == 'genre' or by == 'all':
            sql = text('''
                                select distinct movie_genres.movie_id from movie_genres
                                left join genres on genres.id = movie_genres.genre_id
                                where genres.name like "{}"
                            '''.format(search))
            q3 = self._session_cm.session.query(Movie).filter(Movie._id.in_(select([text('movie_id')]).select_from(sql.columns())))
            if q:
                q = q.union(q3)
            else:
                q = q3
        if by == 'director' or by == 'all':
            sql = text('''
                                select distinct movie_directors.movie_id from movie_directors
                                left join directors on directors.id = movie_directors.director_id
                                where directors.full_name like "{}"
                            '''.format(search))
            q4 = self._session_cm.session.query(Movie).filter(Movie._id.in_(select([text('movie_id')]).select_from(sql.columns())))
            if q:
                q = q.union(q4)
            else:
                q = q4
        data = q.all()
        start = (page - 1) * size
        end = page * size
        total = len(data)
        totalPage = math.ceil(len(data) / size)
        if start > total:
            start = total
        if end > total:
            end = total
        return {
            'movies': data[start:end],
            'total': total,
            'totalPage': totalPage,
            'page': page,
            'size': size
        }

    def add_watch(self, watchList):
        with self._session_cm as scm:
            scm.session.add(watchList)
            scm.commit()

    def remove_watch(self, user, movie):
        with self._session_cm as scm:
            user.watchList.remove(movie)
            scm.session.merge(user)
            scm.commit()

    def add_review(self, review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_poster(self, movie:Movie):
        try:
            res = requests.get('http://www.omdbapi.com', params={
                't': movie.title,
                'y': movie.year,
                'type': 'movie',
                'apikey': '52c4f1cd'
            })
            data = res.json()
            if data.get('Response'):
                movie._poster = data.get('Poster')
                with self._session_cm as scm:
                    scm.session.merge(movie)
                    scm.commit()
        except Exception as e:
            pass

def load_genres(session, data_path: str):
    genres = {}
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csvfile:
        movie_file_reader = csv.DictReader(csvfile)

        for row in movie_file_reader:
            for item in row['Genre'].split(','):
                item = item.strip()
                if item not in genres.keys():
                    genre = Genre(item)
                    genres[item] = genre
                    session.add(genre)
        session.commit()
    return genres

def load_actors(session, data_path: str):
    actors = {}
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csvfile:
        movie_file_reader = csv.DictReader(csvfile)

        for row in movie_file_reader:
            for item in row['Actors'].split(','):
                item = item.strip()
                if item not in actors.keys():
                    actor = Actor(item)
                    actors[item] = actor
                    session.add(actor)
        session.commit()
    return actors

def load_directors(session, data_path: str):
    directors = {}
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csvfile:
        movie_file_reader = csv.DictReader(csvfile)

        for row in movie_file_reader:
            for item in row['Director'].split(','):
                item = item.strip()
                if item not in directors.keys():
                    director = Director(item)
                    directors[item] = director
                    session.add(director)
        session.commit()
    return directors

def parse_float(s):
    v = None
    try:
        v = float(s)
    except ValueError:
        pass
    return v

def load_movies(session, data_path: str):
    genres_dict = load_genres(session, data_path)
    directors_dict = load_directors(session, data_path)
    actors_dict = load_actors(session, data_path)
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csvfile:
        movie_file_reader = csv.DictReader(csvfile)

        for row in movie_file_reader:
            rank = int(row['Rank'])
            title = row['Title']
            genre = [genres_dict.get(item.strip()) for item in row['Genre'].split(',')]
            description = row['Description']
            director = [directors_dict.get(item.strip()) for item in row['Director'].split(',')]
            actors = [actors_dict.get(item.strip()) for item in row['Actors'].split(',')]
            year = int(row['Year'])
            runtime = parse_float(row['Runtime (Minutes)'])
            rating = parse_float(row['Rating'])
            votes = int(row['Votes'])
            revenue = parse_float(row['Revenue (Millions)'])
            metascore = parse_float(row['Metascore'])
            movie = Movie(rank, title, genre, description, director, actors, year, runtime, rating, votes, revenue, metascore)
            yield movie

def populate(session_factory, data_path):
    session = session_factory()
    movie_file_reader = load_movies(session, data_path)
    for movie in movie_file_reader:
        session.add(movie)
    session.commit()