import sqlite3

def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="food_impact_db"
    )

    return connection