def analyze_food(food):

    food_data = {
        "pizza": {"calories": 285, "category": "junk"},
        "salad": {"calories": 120, "category": "healthy"},
        "burger": {"calories": 350, "category": "junk"},
        "idli": {"calories": 70, "category": "healthy"}
    }

    food = food.lower()

    if food in food_data:
        data = food_data[food]

        health_score = 80 if data["category"] == "healthy" else 40

        return {
            "food": food,
            "calories": data["calories"],
            "category": data["category"],
            "health_score": health_score
        }

    return {
        "food": food,
        "calories": 0,
        "category": "unknown",
        "health_score": 50
    }