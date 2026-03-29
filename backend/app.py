import sys
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3

# =============================
# PATH SETUP
# =============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DB_PATH = os.path.join(BASE_DIR, "foodimpact.db")

app = Flask(__name__)
CORS(app)


# =============================
# DB CONNECTION
# =============================

def get_connection():
    return sqlite3.connect(DB_PATH)


# =============================
# CREATE TABLES
# =============================

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # ORDERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        food TEXT,
        price INTEGER,
        category TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # SUPPORT
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS support_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        issue_type TEXT,
        description TEXT,
        status TEXT DEFAULT 'Pending'
    )
    """)

    conn.commit()
    conn.close()


create_tables()


# =============================
# FRONTEND ROUTES
# =============================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "login.html")

@app.route("/login_page")
def login_page():
    return send_from_directory(FRONTEND_DIR, "login.html")

@app.route("/register_page")
def register_page():
    return send_from_directory(FRONTEND_DIR, "register.html")

@app.route("/restaurants_page")
def restaurants_page():
    return send_from_directory(FRONTEND_DIR, "restaurants.html")

@app.route("/menu_page")
def menu_page():
    return send_from_directory(FRONTEND_DIR, "menu.html")

@app.route("/cart_page")
def cart_page():
    return send_from_directory(FRONTEND_DIR, "cart.html")

@app.route("/payment_page")
def payment_page():
    return send_from_directory(FRONTEND_DIR, "payment.html")

@app.route("/dashboard_page")
def dashboard_page():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")

@app.route("/account_page")
def account_page():
    return send_from_directory(FRONTEND_DIR, "account.html")

@app.route("/admin_page")
def admin_page():
    return send_from_directory(FRONTEND_DIR, "admin.html")


# =============================
# STATIC FILES
# =============================

@app.route("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "css"), filename)

@app.route("/js/<path:filename>")
def serve_js(filename):
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
            "INSERT INTO users (name,email,password) VALUES (?,?,?)",
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
        return jsonify({
            "message": "Login successful",
            "user_id": user[0]
        })
    return jsonify({"message": "Invalid credentials"})



# =============================
# PLACE ORDER
# =============================

@app.route("/place_order", methods=["POST"])
def place_order():

    try:
        data = request.json
        print("DATA RECEIVED:", data)

        email = data.get("email")
        cart = data.get("cart", [])

        if not email or not cart:
            return jsonify({"error": "Missing data"}), 400

        food_category = {
            "pizza": "junk",
            "burger": "junk",
            "fried chicken": "junk",
            "salad": "healthy",
            "idli": "healthy",
            "dosa": "healthy"
        }

        conn = get_connection()
        cursor = conn.cursor()

        for item in cart:

            food = item.get("name") or item.get("food")
            price = item.get("price") or item.get("cost") or 0

            if not food:
                continue

            category = food_category.get(food.lower(), "junk")

            cursor.execute("""
                INSERT INTO orders (user_id, food_name, price, category, status)
                VALUES (?,?,?,?,?)
            """, (user_id, food, price, category, "ordered"))

        conn.commit()
        conn.close()

        return jsonify({"message": "Order saved"})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# =============================
# DASHBOARD DATA
# =============================

@app.route("/dashboard_data/<int:user_id>")
def dashboard_data(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(price) FROM orders WHERE user_id=?", (user_id,))
    total = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM orders WHERE user_id=? AND category='healthy'", (user_id,))
    healthy = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE user_id=? AND category='junk'", (user_id,))
    junk = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "calories": total,
        "healthy": healthy,
        "junk": junk
    })

# =============================
# ORDER HISTORY
# =============================

@app.route("/get_orders/<email>")
def get_orders(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT food, price, category, time FROM orders WHERE email=?",
        (email,)
    )

    data = cursor.fetchall()
    conn.close()

    return jsonify(data)


# =============================
# SUPPORT SYSTEM
# =============================

@app.route("/submit_issue", methods=["POST"])
def submit_issue():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO support_requests (user_email, issue_type, description)
        VALUES (?,?,?)
    """, (data["email"], data["issue"], data["description"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Issue submitted"})


# =============================
# ADMIN PANEL
# =============================

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

    cursor.execute(
        "UPDATE support_requests SET status='Resolved' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Resolved"})

@app.route("/support_page")
def support_page():
    return send_from_directory(FRONTEND_DIR, "support.html")

@app.route("/forgot_password_page")
def forgot_password_page():
    return send_from_directory(FRONTEND_DIR, "forgot_password.html")


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

# =============================
# RUN SERVER
# =============================

if __name__ == "__main__":
    app.run(debug=True)