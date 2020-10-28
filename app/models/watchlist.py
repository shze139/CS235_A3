class WatchList:
    def __init__(self, user, movie):
        self._user = user
        self._movie = movie

    @property
    def user(self):
        return self._user

    @property
    def movie(self):
        return self._movie