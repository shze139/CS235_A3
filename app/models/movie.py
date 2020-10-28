from typing import List
from .genre import Genre
from .actor import Actor
from .director import Director
from .review import Review
import requests

class Movie:
    def __init__(self, rank: int, title: str,
                 genre: List[Genre], description: str, director: List[Director],
                 actors: List[Actor], year: int, runtime: float,
                 rating: float,votes: int, revenue:float, metascore:int):
        self._id = None
        self._rank = rank
        self._title = title
        self._genre = genre
        self._description = description
        self._director = director
        self._actors = actors
        self._year = year
        self._runtime = runtime
        self._rating = rating
        self._votes = votes
        self._revenue = revenue
        self._metascore = metascore
        self._poster = None
        self._reviews:List[Review] = list()

    @property
    def id(self) -> int:
        return self._id

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def title(self) -> str:
        return self._title

    @property
    def genre(self) -> List[Genre]:
        return self._genre

    @property
    def description(self) -> str:
        return self._description

    @property
    def director(self) -> List[Director]:
        return self._director

    @property
    def actors(self) -> List[Actor]:
        return self._actors

    @property
    def year(self) -> int:
        return self._year

    @property
    def runtime(self) -> float:
        return self._runtime

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def votes(self) -> int:
        return self._votes

    @property
    def revenue(self) -> float:
        return self._revenue

    @property
    def metascore(self) -> float:
        return self._metascore

    @property
    def poster(self) -> str:
        return self._poster

    @property
    def reviews(self) -> List[Review]:
        return self._reviews

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self._id == other._id


