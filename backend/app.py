import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database.db_connection import get_connection
from datetime import datetime
import webbrowser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__)
CORS(app)

# =============================
# PAGES
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

@app.route("/food_input_page")
def food_input_page():
    return send_from_directory(FRONTEND_DIR, "food_input.html")

@app.route("/dashboard_page")
def dashboard_page():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")

# =============================
# STATIC FILES
# =============================

@app.route("/css/<path:filename>")
def css_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "css"), filename)

@app.route("/js/<path:filename>")
def js_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "js"), filename)

# =============================
# REGISTER
# =============================

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (data["name"], data["email"], data["password"])
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    except:
        return jsonify({"message": "Email already registered"})
    finally:
        conn.close()

# =============================
# LOGIN
# =============================

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"})

# =============================
# FOOD ORDER + ANALYSIS
# =============================

@app.route("/analyze_food", methods=["POST"])
def analyze_food():

    data = request.json
    food = data["food"].lower()
    email = data.get("email", "guest")

    food_data = {
        "pizza": {"calories": 285, "category": "junk", "price": 200},
        "burger": {"calories": 350, "category": "junk", "price": 150},
        "salad": {"calories": 120, "category": "healthy", "price": 120},
        "idli": {"calories": 70, "category": "healthy", "price": 80}
    }

    if food in food_data:

        calories = food_data[food]["calories"]
        category = food_data[food]["category"]
        price = food_data[food]["price"]
        health_score = 80 if category == "healthy" else 40

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO orders (user_email, food_name, price, category, calories, order_time)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            email,
            food,
            price,
            category,
            calories,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "food": food,
            "calories": calories,
            "category": category,
            "health_score": health_score,
            "price": price
        })

    return jsonify({
        "food": food,
        "calories": 0,
        "category": "unknown",
        "health_score": 50,
        "price": 0
    })

# =============================
# RUN
# =============================

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)

@app.route("/reset_page")
def reset_page():
    return send_from_directory(FRONTEND_DIR, "reset.html")

@app.route("/reset_password", methods=["POST"])
def reset_password():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        (data["password"], data["email"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Password updated successfully"})

@app.route("/account_page")
def account_page():
    return send_from_directory(FRONTEND_DIR, "account.html")

@app.route("/get_orders/<email>")
def get_orders(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT food_name, price, category, order_time FROM orders WHERE user_email=?",
        (email,)
    )

    data = cursor.fetchall()
    conn.close()

    return jsonify(data)

@app.route("/support_page")
def support_page():
    return send_from_directory(FRONTEND_DIR, "support.html")

@app.route("/submit_issue", methods=["POST"])
def submit_issue():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO support_requests (user_email, issue_type, description)
    VALUES (?, ?, ?)
    """, (
        data["email"],
        data["issue"],
        data["description"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Issue submitted successfully"})

@app.route("/admin_page")
def admin_page():
    return send_from_directory(FRONTEND_DIR, "admin.html")

@app.route("/get_issues")
def get_issues():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM support_requests")
    data = cursor.fetchall()

    conn.close()

    return jsonify(data)

@app.route("/resolve_issue/<int:id>", methods=["POST"])
def resolve_issue(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE support_requests SET status='Resolved' WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return jsonify({"message": "Resolved"})