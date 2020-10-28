from app.models.user import User

class UsernameNotUniqueException(Exception):
    pass

class LoginFailedException(Exception):
    pass

def register(username, password, repo):
    user = repo.get_user(username)
    if user is not None:
        raise UsernameNotUniqueException

    user = User(username, password)
    repo.add_user(user)

def login(username, password, repo):
    user = repo.get_user(username)
    if user is None or user.password != password:
        raise LoginFailedException
    return user