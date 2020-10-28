
class Genre:
    def __init__(self, name: str):
        self._id = None
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return (
            self._name == other._name
        )


