import os
import psycopg


def connect():
    try:
        config = 'dbname={0} user={1} password={2} host={3} port={4}'.format(
            os.environ.get('DB_NAME'),
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            os.environ.get('DB_HOST'),
            os.environ.get('DB_PORT')
        )
        return {'config': config}
        with psycopg.connect(config) as conn:
            return conn

    except (psycopg.DatabaseError, Exception) as e:
        print(e)


