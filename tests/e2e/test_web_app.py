
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Movies App' in response.data

def test_search(client):
    search_result_tpl = 'Found <span class="is-error">{}</span> movies for <strong>{}</strong> by <strong>{}</strong>'

    page = 1
    size = 50
    # search by all
    by = 'all'
    key = 'Guardians of the Galaxy'
    result_count = 1
    response = client.get('/', query_string={
        'page': page,
        'size': size,
        'by': by,
        'key': key
    })
    assert response.status_code == 200
    assert search_result_tpl.format(result_count, key, by).encode() in response.data

    # search by actor
    by = 'actor'
    key = 'Chris Pratt'
    result_count = 7
    response = client.get('/', query_string={
        'page': page,
        'size': size,
        'by': by,
        'key': key
    })
    assert response.status_code == 200
    assert search_result_tpl.format(result_count, key, by).encode() in response.data

def test_movie_detail(client):
    movieId = 1
    movieTitle = b'Guardians of the Galaxy'
    moviePoster = b'https://m.media-amazon.com/images/M/MV5BMTAwMjU5OTgxNjZeQTJeQWpwZ15BbWU4MDUxNDYxODEx._V1_SX300.jpg'
    response = client.get('/movie/{}'.format(movieId))

    assert response.status_code == 200
    assert b'Movie Detail' in response.data
    assert movieTitle in response.data
    # assert moviePoster in response.data

    # test not found
    movieId = 9999
    response = client.get('/movie/{}'.format(movieId))
    assert response.status_code == 404
    assert b'Movie not found' in response.data


def test_register(client, auth):
    # register page
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data

    # register successful
    username = 'jack'
    password = '123456'
    response = auth.register(username, password)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Register successful' in response.data

    # register username has been used
    response = auth.register(username, password)
    assert response.status_code == 200
    assert b'Register' in response.data
    assert b'Username has been used.' in response.data

    # register password error
    username1 = 'tom'
    password1 = '123'
    response = auth.register(username1, password1)
    assert response.status_code == 200
    assert b'Register' in response.data
    assert b'Passwords must be at least 6 characters.' in response.data


def test_login(client, auth):
    # login page
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data

    # register
    # username: jack password: 123456
    username = 'jack'
    password = '123456'
    auth.register(username, password)

    # login error
    error_password = '1234561'
    response = auth.login(username, error_password)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username or password is error' in response.data

    # login success
    response = auth.login(username, password)
    assert response.status_code == 200
    assert b'Movies App' in response.data
    assert username.encode() in response.data

    # logout
    response = auth.logout()
    assert response.status_code == 200
    assert b'Movies App' in response.data
    assert username.encode() not in response.data


def test_review(client, auth):
    auth.register()
    auth.login()

    movieId = 1
    movieTitle = b'Guardians of the Galaxy'

    # check reviews before add
    response = client.get('/movie/{}'.format(movieId))
    assert response.status_code == 200
    assert movieTitle in response.data
    assert b'Movie Reviews(0)' in response.data

    # add first review
    review_content1 = 'first review'
    response = client.post('/movie/add_review/{}'.format(movieId), data={
        'content': review_content1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert movieTitle in response.data
    assert review_content1.encode() in response.data
    assert b'add review successful' in response.data
    assert b'Movie Reviews(1)' in response.data

    # add second review
    review_content2 = 'second review'
    response = client.post('/movie/add_review/{}'.format(movieId), data={
        'content': review_content2
    },follow_redirects=True)
    assert response.status_code == 200
    assert movieTitle in response.data
    assert review_content2.encode() in response.data
    assert b'add review successful' in response.data
    assert b'Movie Reviews(2)' in response.data

    # add empty review
    review_content3 = ''
    response = client.post('/movie/add_review/{}'.format(movieId), data={
        'content': review_content3
    },follow_redirects=True)
    assert response.status_code == 200
    assert movieTitle in response.data
    assert b'review content cannot be empty' in response.data

def test_watchlist(client, auth):
    auth.register()
    auth.login()

    movieId = 1
    movieTitle = b'Guardians of the Galaxy'

    # not watch
    response = client.get('/movie/{}'.format(movieId))
    assert response.status_code == 200
    assert movieTitle in response.data
    assert b'Add To WatchList' in response.data

    # add a movie to watchlsit
    response = client.get('/movie/add_to_watchlist/{}'.format(movieId), follow_redirects=True)
    assert response.status_code == 200
    assert movieTitle in response.data
    assert b'Remove From WatchList' in response.data

    response = client.get('/movie/watchlist'.format(movieId))
    assert response.status_code == 200
    assert b'WatchList' in response.data
    assert movieTitle in response.data

    # remove a movie from watchlsit
    response = client.get('/movie/remove_from_watchlist/{}'.format(movieId), follow_redirects=True)
    assert response.status_code == 200
    assert movieTitle in response.data
    assert b'Add To WatchList' in response.data

def test_not_login_watchlist(client):
    response = client.get('/movie/watchlist', follow_redirects=True)

    assert response.status_code == 200
    assert b'You need to login first.' in response.data

def test_not_login_review(client):
    response = client.get('/movie/1')

    assert response.status_code == 200
    assert b'Login to add a review.' in response.data

def test_login_review(client, auth):
    auth.register()
    auth.login()

    response = client.get('/movie/1')

    assert response.status_code == 200
    assert b'<button>Add</button>' in response.data


