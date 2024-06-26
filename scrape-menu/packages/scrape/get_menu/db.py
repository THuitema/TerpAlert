import os
import psycopg


def connect():
    try:
        config = 'dbname={0} user={1} password={2} host={3} port={4}'.format(
            os.environ.get('database'),
            os.environ.get('username'),
            os.environ.get('password'),
            os.environ.get('host'),
            os.environ.get('port')
        )
        with psycopg.connect(config) as conn:
            return conn

    except (psycopg.DatabaseError, Exception) as e:
        print(e)


