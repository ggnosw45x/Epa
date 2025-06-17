import sqlite3
import threading

db_lock = threading.Lock()

def connect_to_db():
    conn = sqlite3.connect('kurama.db', check_same_thread=False)
    return conn
