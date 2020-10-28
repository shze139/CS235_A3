from sqlalchemy import inspect

def test_table_names(database_engine):

    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['actors', 'directors', 'genres', 'movie_actors', 'movie_directors', 'movie_genres', 'movies', 'reviews', 'users', 'watchlist']

def test_movies(database_engine):
    with database_engine.connect() as connection:
        result = connection.execute('select count(*) from movies').first()
        assert result[0] == 1000

        title = 'Guardians of the Galaxy'
        result = connection.execute('select title from movies where rank = 1').first()
        assert result[0] == title

def test_movies_actors(database_engine):
    with database_engine.connect() as connection:
        result = connection.execute('''
            select actors.full_name from movie_actors left join actors on movie_actors.actor_id == actors.id
            where movie_actors.movie_id = 1
        ''')

        actors1 = []
        for row in result:
            actors1.append(row[0])

        actors2 = ['Chris Pratt' , 'Vin Diesel' , 'Bradley Cooper' , 'Zoe Saldana']

        assert actors1 == actors2

def test_genre(database_engine):
    with database_engine.connect() as connection:
        result = connection.execute('''
            select genres.name from movie_genres left join genres on movie_genres.genre_id == genres.id
            where movie_genres.movie_id = 1
        ''')

        genres1 = []
        for row in result:
            genres1.append(row[0])

        genres2 = ['Action' , 'Adventure' , 'Sci-Fi']

        assert genres1 == genres2

def test_director(database_engine):
    with database_engine.connect() as connection:
        result = connection.execute('''
            select directors.full_name from movie_directors left join directors on movie_directors.director_id == directors.id
            where movie_directors.movie_id = 1
        ''')

        directors1 = []
        for row in result:
            directors1.append(row[0])

        directors2 = ['James Gunn']

        assert directors1 == directors2




