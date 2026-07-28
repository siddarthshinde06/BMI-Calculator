"""
Simple BMI calculation helpers.
Everything is converted to metric (kg, metres) before calculating,
so the rest of the app never has to worry about units.
"""

def to_kg(weight, unit):
    """Convert weight to kilograms."""
    if unit == "kg":
        return weight
    if unit == "g":
        return weight / 1000
    if unit == "lb":
        return weight * 0.45359237
    if unit == "stone":
        # 'weight' passed in as total pounds already (stones converted on frontend/route)
        return weight * 0.45359237
    raise ValueError("Unknown weight unit")


def to_metres(height, unit):
    """Convert height to metres."""
    if unit == "m":
        return height
    if unit == "cm":
        return height / 100
    if unit == "mm":
        return height / 1000
    if unit == "inches":
        return height * 0.0254
    raise ValueError("Unknown height unit")


def calculate_bmi(weight_kg, height_m):
    """Standard BMI formula: weight(kg) / height(m)^2"""
    return round(weight_kg / (height_m ** 2), 1)


def calculate_bmi_prime(bmi):
    """BMI Prime = BMI / 25 (the upper limit of 'normal')"""
    return round(bmi / 25, 2)


def calculate_ponderal_index(weight_kg, height_m):
    """Ponderal Index = weight(kg) / height(m)^3"""
    return round(weight_kg / (height_m ** 3), 1)


def get_category(bmi):
    """Return the BMI category name."""
    if bmi < 16:
        return "Severe Underweight"
    elif bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    elif bmi < 35:
        return "Obesity Class I"
    elif bmi < 40:
        return "Obesity Class II"
    else:
        return "Obesity Class III"


def get_risk_level(category):
    """Map category to a simple health-risk label."""
    mapping = {
        "Severe Underweight": "High",
        "Underweight": "Moderate",
        "Normal weight": "Low",
        "Overweight": "Moderate",
        "Obesity Class I": "High",
        "Obesity Class II": "Very High",
        "Obesity Class III": "Extremely High",
    }
    return mapping.get(category, "Unknown")


def healthy_weight_range(height_m):
    """Weight range (kg) that corresponds to a BMI of 18.5–24.9."""
    low = round(18.5 * height_m ** 2, 1)
    high = round(24.9 * height_m ** 2, 1)
    return low, high


def weight_to_goal(weight_kg, height_m):
    """How many kg to lose/gain to reach the healthy range midpoint."""
    low, high = healthy_weight_range(height_m)
    if weight_kg < low:
        return round(low - weight_kg, 1), "gain"
    elif weight_kg > high:
        return round(weight_kg - high, 1), "lose"
    else:
        return 0, "maintain"


def estimate_calories(weight_kg, height_m, age, gender):
    """
    Rough daily calorie estimate using the Mifflin-St Jeor formula
    (assumes light activity, so multiplied by 1.375).
    Falls back to sensible defaults if age/gender are missing.
    """
    age = age or 30
    height_cm = height_m * 100
    if gender == "female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:  # default to male formula if unspecified
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return round(bmr * 1.375)


def estimate_protein(weight_kg):
    """Rough daily protein need in grams (0.8-1g per kg is a common guideline)."""
    return round(weight_kg * 0.9)


def estimate_water(weight_kg):
    """Rough daily water intake in litres (~33ml per kg)."""
    return round(weight_kg * 0.033, 1)
