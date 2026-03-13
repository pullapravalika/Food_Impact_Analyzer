import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "foodimpact.db")

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    return connection