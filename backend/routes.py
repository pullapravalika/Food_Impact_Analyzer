from flask import request, jsonify
from auth import register_user, login_user
from food_analysis import analyze_food
from database.db_connection import get_connection


def register_routes(app):

    @app.route("/register", methods=["POST"])
    def register():
        data = request.json
        return register_user(data)


    @app.route("/login", methods=["POST"])
    def login():
        data = request.json
        return login_user(data)


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