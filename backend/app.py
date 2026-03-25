import sys
import os
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from database.db_connection import get_connection
from backend.order_api import order_bp

# =============================
# APP SETUP
# =============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__)
CORS(app)

app.register_blueprint(order_bp)

# =============================
# PAGE ROUTES (ALL FIXED ✅)
# =============================

@app.route("/")
@app.route("/home")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


# LOGIN
@app.route("/login_page")
@app.route("/login.html")
def login_page():
    return send_from_directory(FRONTEND_DIR, "login.html")


# REGISTER
@app.route("/register_page")
@app.route("/register.html")
def register_page():
    return send_from_directory(FRONTEND_DIR, "register.html")


# ACCOUNT (NEW FIX 🔥)
@app.route("/account_page")
@app.route("/account.html")
def account_page():
    return send_from_directory(FRONTEND_DIR, "account.html")


@app.route("/restaurants_page")
def restaurants_page():
    return send_from_directory(FRONTEND_DIR, "restaurants.html")

# FOOD INPUT
@app.route("/food_input_page")
@app.route("/food_input.html")
def food_input_page():
    return send_from_directory(FRONTEND_DIR, "food_input.html")


# MENU
@app.route("/menu_page")
@app.route("/menu.html")
def menu_page():
    return send_from_directory(FRONTEND_DIR, "menu.html")


# CART
@app.route("/cart_page")
@app.route("/cart.html")
def cart_page():
    return send_from_directory(FRONTEND_DIR, "cart.html")


# DASHBOARD
@app.route("/dashboard_page")
@app.route("/dashboard.html")
def dashboard_page():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")


# ADMIN
@app.route("/admin_page")
@app.route("/admin.html")
def admin_page():
    return send_from_directory(FRONTEND_DIR, "admin.html")


# SUPPORT
@app.route("/support_page")
@app.route("/support.html")
def support_page():
    return send_from_directory(FRONTEND_DIR, "support.html")


# ORDER SUCCESS
@app.route("/order_success_page")
@app.route("/order_success.html")
def order_success():
    return send_from_directory(FRONTEND_DIR, "order_success.html")


# RECOVERY
@app.route("/forgot_password_page")
@app.route("/recovery.html")
def recovery_page():
    return send_from_directory(FRONTEND_DIR, "recovery.html")


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
# REGISTER API
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
    except Exception:
        return jsonify({"message": "Email already exists"})
    finally:
        cursor.close()
        conn.close()


# =============================
# LOGIN API
# =============================

@app.route("/login", methods=["POST"])
def login():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,name,email FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "user_id": user[0],
            "name": user[1],
            "email": user[2]
        })

    return jsonify({"message": "Invalid credentials"})


# =============================
# RESET PASSWORD
# =============================

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

    message = "Password updated successfully" if cursor.rowcount > 0 else "Email not found"

    cursor.close()
    conn.close()

    return jsonify({"message": message})


# =============================
# SUPPORT SYSTEM
# =============================

@app.route("/submit_complaint", methods=["POST"])
def submit_complaint():
    data = request.json

    conn = sqlite3.connect("support.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints (user_email, issue, description)
        VALUES (?, ?, ?)
    """, (data["email"], data["issue"], data["description"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Complaint submitted successfully"})


@app.route("/get_complaints", methods=["GET"])
def get_complaints():
    conn = sqlite3.connect("support.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    rows = cursor.fetchall()

    conn.close()

    complaints = []
    for row in rows:
        complaints.append({
            "id": row[0],
            "email": row[1],
            "issue": row[2],
            "description": row[3],
            "status": row[4],
            "reply": row[5]
        })

    return jsonify(complaints)


@app.route("/update_complaint", methods=["POST"])
def update_complaint():
    data = request.json

    conn = sqlite3.connect("support.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET status=?, admin_reply=?
        WHERE id=?
    """, (data["status"], data["reply"], data["id"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Reply sent successfully"})


# =============================
# RUN SERVER
# =============================

if __name__ == "__main__":
    app.run(debug=True)