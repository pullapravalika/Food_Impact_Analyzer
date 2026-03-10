import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify
from flask_cors import CORS
from database.db_connection import get_connection

app = Flask(__name__)
CORS(app)


# Home route
@app.route('/')
def home():
    return "Food Impact Analyzer Backend Running"


# Register API
@app.route('/register', methods=['POST'])
def register():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
    values = (data["name"], data["email"], data["password"])

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "User registered successfully"})


# Login API
@app.route('/login', methods=['POST'])
def login():

    data = request.json

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


# Food Analysis API
@app.route('/analyze_food', methods=['POST'])
def analyze_food():

    data = request.json
    food = data["food"].lower()

    food_data = {
        "pizza": {"calories": 285, "category": "junk"},
        "burger": {"calories": 350, "category": "junk"},
        "salad": {"calories": 120, "category": "healthy"},
        "idli": {"calories": 70, "category": "healthy"}
    }

    if food in food_data:

        category = food_data[food]["category"]
        calories = food_data[food]["calories"]
        health_score = 80 if category == "healthy" else 40

        # store in database
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO food_logs (user_id,food_name,calories,category,health_score)
        VALUES (%s,%s,%s,%s,%s)
        """

        values = (1, food, calories, category, health_score)

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "food": food,
            "calories": calories,
            "category": category,
            "health_score": health_score
        })

    return jsonify({
        "food": food,
        "calories": 0,
        "category": "unknown",
        "health_score": 50
    })


if __name__ == "__main__":
    app.run(debug=True)