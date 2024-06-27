import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']


def connect():
    try:
        # config = 'dbname={0} user={1} password={2} host={3} port={4} sslmode=require'.format(
        #     os.environ.get('DB_NAME'),
        #     os.environ.get('DB_USER'),
        #     os.environ.get('DB_PASSWORD'),
        #     os.environ.get('DB_HOST'),
        #     os.environ.get('DB_PORT')
        # )

        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn: # os.environ.get('DB_URL')
            return conn

    except (psycopg2.DatabaseError, Exception) as e:
        print(e)


