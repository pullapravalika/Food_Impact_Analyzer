import sqlite3
from flask import request, jsonify, send_from_directory
from auth import register_user, login_user
from food_analysis import analyze_food
from backend.database.db_connection import get_connection

# If FRONTEND_DIR is not defined, define it (adjust path if needed)
import os
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend")


def register_routes(app):

    # ---------------- REGISTER ----------------
    @app.route("/register", methods=["POST"])
    def register():
        data = request.json
        return register_user(data)


    # ---------------- LOGIN ----------------
    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        return login_user(data)


    # ---------------- FORGOT PASSWORD PAGE ----------------
    @app.route("/forgot_password_page")
    def forgot_password_page():
        return send_from_directory(FRONTEND_DIR, "recovery.html")


    # ---------------- FOOD ANALYSIS ----------------
    @app.route("/analyze_food", methods=["POST"])
    def analyze():

        data = request.json
        result = analyze_food(data["food"])

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO food_logs (user_id, food_name, calories, category, health_score)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            1,
            result["food"],
            result["calories"],
            result["category"],
            result["health_score"]
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify(result)


    # ---------------- SUBMIT COMPLAINT ----------------
    @app.route('/submit_complaint', methods=['POST'])
    def submit_complaint():
        data = request.json

        conn = sqlite3.connect('support.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO complaints (user_email, issue, description)
            VALUES (?, ?, ?)
        """, (data['email'], data['issue'], data['description']))

        conn.commit()
        conn.close()

        return jsonify({"message": "Complaint submitted successfully"})


    # ---------------- GET ALL COMPLAINTS (ADMIN) ----------------
    @app.route('/get_complaints', methods=['GET'])
    def get_complaints():

        conn = sqlite3.connect('support.db')
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


    # ---------------- UPDATE COMPLAINT (ADMIN REPLY) ----------------
    @app.route('/update_complaint', methods=['POST'])
    def update_complaint():

        data = request.json

        conn = sqlite3.connect('support.db')
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE complaints
            SET status = ?, admin_reply = ?
            WHERE id = ?
        """, (data['status'], data['reply'], data['id']))

        conn.commit()
        conn.close()

        return jsonify({"message": "Complaint updated successfully"})