from flask import jsonify

users = []

def register_user(data):

    user = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]
    }

    users.append(user)

    return jsonify({"message": "User registered successfully"})


def login_user(data):

    for user in users:
        if user["email"] == data["email"] and user["password"] == data["password"]:
            return jsonify({"message": "Login successful"})

    return jsonify({"message": "Invalid credentials"})