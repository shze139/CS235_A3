class User:
    def __init__(self, username:str, password:str):
        self._id = None
        self._username = username
        self._password = password
        self._watchList = list()

    @property
    def id(self) -> str:
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def watchList(self):
        return self._watchList

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
            self._username == other._username
            and self._password == other._password
        )
