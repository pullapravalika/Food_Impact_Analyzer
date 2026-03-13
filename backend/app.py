import sys
import os

# Allow project root imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database.db_connection import get_connection
import webbrowser

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__)
CORS(app)


# =============================
# Serve HTML Pages
# =============================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/login_page")
def login_page():
    return send_from_directory(FRONTEND_DIR, "login.html")

@app.route("/register_page")
def register_page():
    return send_from_directory(FRONTEND_DIR, "register.html")


@app.route("/dashboard_page")
def dashboard_page():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")


@app.route("/food_input_page")
def food_input_page():
    return send_from_directory(FRONTEND_DIR, "food_input.html")


# =============================
# Serve Static Files
# =============================

@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "css"), filename)


@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "js"), filename)


# =============================
# Register API
# =============================

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    try:

    query = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
    values = (data["name"], data["email"], data["password"])

        cursor.execute(query, values)
        conn.commit()

        return jsonify({"message": "User registered successfully"})

    except Exception as e:

        return jsonify({"message": "Email already registered"})

    finally:
        cursor.close()
        conn.close()

# =============================
# Login API
# =============================

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE email=? AND password=?"
    cursor.execute(query, (data["email"], data["password"]))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"})


# =============================
# Food Analysis API
# =============================

@app.route("/analyze_food", methods=["POST"])
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

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO food_logs (user_id,food_name,calories,category,health_score)
        VALUES (?,?,?,?,?)
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


# =============================
# Run Server
# =============================

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)