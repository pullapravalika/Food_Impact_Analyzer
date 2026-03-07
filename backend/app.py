from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users = []

# Home route (ADD THIS HERE)
@app.route('/')
def home():
    return "Food Impact Analyzer Backend Running"


# Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    user = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]
    }

    users.append(user)

    return jsonify({"message": "User registered successfully"})


# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    for user in users:
        if user["email"] == data["email"] and user["password"] == data["password"]:
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