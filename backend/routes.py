from flask import request, jsonify
from auth import register_user, login_user
from food_analysis import analyze_food

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
        return jsonify(result)