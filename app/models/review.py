from datetime import datetime

class Review:
    def __init__(self, content: str, timestamp:datetime, user, movie):
        self._id = None
        self._content = content
        self._timestamp = timestamp
        self._userId = None
        self._movieId = None
        self._user = user
        self._movie = movie

    @property
    def id(self) -> int:
        return self._id

    @property
    def content(self) -> str:
        return self._content

    @property
    def timestamp(self) -> datetime:
        return self._timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def userId(self) -> int:
        return self._userId

    @property
    def movieId(self) -> int:
        return self._movieId

    @property
    def user(self):
        return self._user

    @property
    def movie(self):
        return self._movie




