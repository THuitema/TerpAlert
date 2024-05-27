import psycopg2

from config import load_config


def connect():
    # Connect to the PostgreSQL database
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:  # ** ensures arg passed is stored as a dict
            # print('Connected to the server successfully')
            return conn
    except (psycopg2.DatabaseError, Exception) as e:
        print(e)


def db_write(db: psycopg2.extensions.connection, query, *args):
    cur = db.cursor()
    try:
        cur.execute(query, tuple(args))
    except Exception as e:
        print("Query execution unsuccessful: {0}".format(e))

    db.commit()
    cur.close()


def db_select(db: psycopg2.extensions.connection, query, *args):  # fields, table, conditions
    # query = "SELECT {0} FROM \"{1}\" WHERE {2}".format(fields, table, conditions)

    result = []
    cur = db.cursor()

    try:
        cur.execute(query, tuple(args))
        result = cur.fetchall()
    except Exception as e:
        print("Query execution unsuccessful: {0}".format(e))

    cur.close()
    return result

# if __name__ == '__main__':
#     connection = connect()
#
#     connection.close()
