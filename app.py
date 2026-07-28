"""
AI Smart BMI Calculator - Flask backend.

Run with:
    pip install -r requirements.txt
    python app.py

Then open http://127.0.0.1:5000
"""

import json
import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from utils.bmi import (
    to_kg, to_metres, calculate_bmi, calculate_bmi_prime,
    calculate_ponderal_index, get_category, get_risk_level,
    healthy_weight_range, weight_to_goal, estimate_calories,
    estimate_protein, estimate_water,
)

app = Flask(__name__)
CORS(app)

# Load the rule-based recommendation data once at startup
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "recommendations.json")
with open(DATA_PATH, "r") as f:
    RECOMMENDATIONS = json.load(f)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    # Accept either JSON body or form data
    data = request.get_json(silent=True) or request.form

    try:
        height_value = float(data.get("height"))
        height_unit = data.get("height_unit", "cm")
        weight_value = float(data.get("weight"))
        weight_unit = data.get("weight_unit", "kg")

        age = data.get("age")
        age = int(age) if age else None
        gender = data.get("gender") or None
        goal = data.get("goal") or None

        # --- Validation ---
        if height_value <= 0 or weight_value <= 0:
            return jsonify({"error": "Height and weight must be positive numbers."}), 400
        if height_unit == "cm" and not (30 <= height_value <= 300):
            return jsonify({"error": "Please enter a realistic height."}), 400
        if weight_unit == "kg" and not (2 <= weight_value <= 500):
            return jsonify({"error": "Please enter a realistic weight."}), 400

        # --- Convert to metric ---
        height_m = to_metres(height_value, height_unit)
        weight_kg = to_kg(weight_value, weight_unit)

        # --- Core calculations ---
        bmi = calculate_bmi(weight_kg, height_m)
        category = get_category(bmi)
        risk = get_risk_level(category)
        low, high = healthy_weight_range(height_m)
        diff_amount, diff_direction = weight_to_goal(weight_kg, height_m)
        bmi_prime = calculate_bmi_prime(bmi)
        ponderal_index = calculate_ponderal_index(weight_kg, height_m)
        calories = estimate_calories(weight_kg, height_m, age, gender)
        protein = estimate_protein(weight_kg)
        water = estimate_water(weight_kg)

        # --- Recommendation lookup (rule-based, no external AI) ---
        # Collapse detailed categories into the 4 broad buckets used in recommendations.json
        if "Underweight" in category:
            rec_key = "Underweight"
        elif category == "Normal weight":
            rec_key = "Normal weight"
        elif category == "Overweight":
            rec_key = "Overweight"
        else:
            rec_key = "Obese"

        recommendation = RECOMMENDATIONS.get(rec_key, {})

        return jsonify({
            "bmi": bmi,
            "category": category,
            "risk_level": risk,
            "healthy_weight_range": {"low": low, "high": high},
            "weight_goal": {"amount": diff_amount, "direction": diff_direction},
            "bmi_prime": bmi_prime,
            "ponderal_index": ponderal_index,
            "daily_calories": calories,
            "daily_protein_g": protein,
            "daily_water_l": water,
            "recommendation": recommendation,
            "goal": goal,
        })

    except (TypeError, ValueError):
        return jsonify({"error": "Please enter valid numeric values for height and weight."}), 400


@app.route("/health-guide")
def health_guide():
    return jsonify(RECOMMENDATIONS)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
