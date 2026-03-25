import sqlite3

def connect_db():
    return sqlite3.connect('support.db')

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            issue TEXT,
            description TEXT,
            status TEXT DEFAULT 'Pending',
            admin_reply TEXT
        )
    """)

    conn.commit()
    conn.close()

create_table()