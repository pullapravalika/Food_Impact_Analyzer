from flask import Blueprint, request, jsonify
from database.db_connection import get_connection

order_bp = Blueprint("orders", __name__)


# PLACE ORDER
@order_bp.route("/place_order", methods=["POST"])
def place_order():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO orders (user_id, food_name, price, category, status)
    VALUES (?, ?, ?, ?, ?)
    """

    values = (
        data["user_id"],
        data["food_name"],
        data["price"],
        data["category"],
        "ordered"
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Order placed successfully"})


# GET ORDER HISTORY
@order_bp.route("/orders/<int:user_id>", methods=["GET"])
def get_orders(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT food_name, price, status, order_time FROM orders WHERE user_id=?"

    cursor.execute(query, (user_id,))
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    result = []

    for order in orders:

        result.append({
            "food": order[0],
            "price": order[1],
            "status": order[2],
            "time": order[3]
        })

    return jsonify(result)