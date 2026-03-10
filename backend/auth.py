from flask import jsonify
from database.db_connection import get_connection


def register_user(data):

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values = (data["name"], data["email"], data["password"])

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "User registered successfully"})


def login_user(data):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(query, (data["email"], data["password"]))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"})