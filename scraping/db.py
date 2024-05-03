import psycopg2
from config import load_config


def connect(config):
    # Connect to the PostgreSQL database
    try:
        with psycopg2.connect(**config) as conn:  # ** ensures arg passed is stored as a dict
            print('Connected to the server successfully')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    config = load_config()
    connect(config)