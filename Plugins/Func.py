import sqlite3

def connect_to_db():
    conn = sqlite3.connect('kurama.db', timeout=10)
    return conn
