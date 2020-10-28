import abc
from typing import List
from datetime import date

from ..models.movie import Movie
from ..models.user import User
from ..models.review import Review
from ..models.watchlist import WatchList


repo_instance = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int) -> Movie:
        raise NotImplementedError

    @abc.abstractmethod
    def search_movies(self, key:str, by:str, page:int = 1, size:int = 15) -> List[Movie]:
        raise NotImplementedError

    def add_watch(self, watchList:WatchList):
        raise NotImplementedError

    def remove_watch(self, user:User, movie:Movie):
        raise NotImplementedError

    def add_review(self, review:Review):
        raise NotImplementedError

    def get_poster(self, movie:Movie):
        raise NotImplementedError

