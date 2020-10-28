
class Director:

    def __init__(self, full_name: str):
        self._id = None
        self._full_name = full_name

    @property
    def id(self) -> int:
        return self._id

    @property
    def full_name(self) -> str:
        return self._full_name

    def __eq__(self, other):
        if not isinstance(other, Director):
            return False
        return (
            self._full_name == other._full_name
        )