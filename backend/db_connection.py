import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="CFP project",
        user="postgres",
        password="DekDe579",
        host="localhost",
        port="5432"
    )
    return conn
