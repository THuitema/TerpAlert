import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']


def connect() -> psycopg2.extensions.connection:
    """
    :return: conection to PostgreSQL database
    """
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            return conn

    except (psycopg2.DatabaseError, Exception) as e:
        print(e)


def db_write(db: psycopg2.extensions.connection, query, *args):
    """
    Execute a write operation on the database connection
    :param db: PostgreSQL database connection
    :param query: SQL query
    :param args: variables for query
    """
    cur = db.cursor()
    try:
        cur.execute(query, tuple(args))
    except Exception as e:
        print("Query execution unsuccessful: {0}".format(e))

    db.commit()
    cur.close()


def db_select(db: psycopg2.extensions.connection, query, *args):
    """
    Execute read operation on the database connection
    :param db: PostgreSQL database connection
    :param query: SQL query
    :param args: variables for query
    :return:
    """
    result = []
    cur = db.cursor()

    try:
        cur.execute(query, tuple(args))
        result = cur.fetchall()
    except Exception as e:
        print("Query execution unsuccessful: {0}".format(e))

    cur.close()
    return result
