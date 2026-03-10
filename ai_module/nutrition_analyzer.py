import pandas as pd

data = pd.read_csv("data/food_nutrition_dataset.csv")

def analyze_food(food_name):

    food_name = food_name.lower()

    food = data[data["food"] == food_name]

    if food.empty:
        return {"error": "Food not found"}

    calories = int(food["calories"].values[0])
    protein = float(food["protein"].values[0])
    carbs = float(food["carbs"].values[0])
    fat = float(food["fat"].values[0])

    health_score = 100 - (fat * 2 + carbs * 0.5)

    if health_score >= 75:
        category = "Healthy"
    elif health_score >= 50:
        category = "Moderate"
    else:
        category = "Junk"

    return {
        "food": food_name,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "health_score": round(health_score,2),
        "category": category
    }