import sys
import os

# ADD PROJECT ROOT TO PYTHON PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Register order blueprint
app.register_blueprint(order_bp)


# =============================
# PAGE ROUTES
# =============================

@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/login_page")
@app.route("/login.html")
def login_page():
    return send_from_directory(FRONTEND_DIR, "login.html")

@app.route("/forgot_password_page")
def forgot_password_page():
    return send_from_directory(FRONTEND_DIR, "recovery.html")


@app.route("/register_page")
@app.route("/register.html")
def register_page():
    return send_from_directory(FRONTEND_DIR, "register.html")


@app.route("/restaurants_page")
@app.route("/restaurants.html")
def restaurants_page():
    return send_from_directory(FRONTEND_DIR, "restaurants.html")


@app.route("/menu")
@app.route("/menu.html")
def menu_page():
    return send_from_directory(FRONTEND_DIR, "menu.html")


@app.route("/cart")
@app.route("/cart.html")
def cart_page():
    return send_from_directory(FRONTEND_DIR, "cart.html")


@app.route("/dashboard_page")
@app.route("/dashboard.html")
def dashboard_page():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")


@app.route("/payment.html")
def payment_page():
    return send_from_directory(FRONTEND_DIR, "payment.html")


@app.route("/order_success.html")
def order_success():
    return send_from_directory(FRONTEND_DIR, "order_success.html")


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
    name = data["name"]
    email = data["email"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES (?,?,?)",
            (name, email, password)
        )

        conn.commit()

        return jsonify({"message": "User registered successfully"})

    except Exception:
        return jsonify({"message": "Email already exists"})

    finally:
        cursor.close()
        conn.close()


\

# =============================
# LOGIN API
# =============================

@app.route("/login", methods=["POST"])
def login():

    data = request.json
    email = data.get("email")
    password = data.get("password")
    print("LOGIN TRY:", email, password)   # DEBUG LINE
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,name,email FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    print("DB RESULT:", user)  # DEBUG LINE
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
# RESET PASSWORD API
# =============================

@app.route("/reset_password", methods=["POST"])
def reset_password():

    data = request.json
    email = data.get("email")
    new_password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        (new_password, email)
    )

    conn.commit()

    if cursor.rowcount > 0:
        message = "Password updated successfully"
    else:
        message = "Email not found"

    cursor.close()
    conn.close()

    return jsonify({"message": message})


# =============================
# FOOD ANALYSIS API
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
# RUN SERVER
# =============================

if __name__ == "__main__":
    app.run(debug=True)