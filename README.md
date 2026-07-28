# 🩺 AI Smart BMI Calculator

A modern, full-featured **BMI Calculator** built with **Python (Flask)** on the backend and **HTML, CSS, and vanilla JavaScript** on the frontend. It goes beyond a basic BMI number — calculating detailed health metrics and offering intelligent, rule-based recommendations tailored to your BMI category.

> ⚠️ **Disclaimer:** This application is intended for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-black?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

---

## ✨ Features

| Category | Details |
|---|---|
| 📏 **Units** | Full support for both **Metric** and **Imperial** measurement systems |
| 📊 **Core Metrics** | BMI, BMI Category, and Health Risk Level |
| ⚖️ **Weight Insights** | Healthy Weight Range & Weight Gain/Loss required to reach it |
| 📐 **Advanced Metrics** | BMI Prime & Ponderal Index |
| 🥗 **Nutrition** | Rule-based food recommendations, daily protein & calorie needs |
| 🥛 **Hydration** | Estimated daily water intake |
| 💪 **Fitness** | Personalized exercise suggestions |
| 🌙 **UX** | Dark mode, fully responsive design, and print-friendly BMI reports |
| 💾 **History** | Saves recent calculations locally (Local Storage) |

---

## 🛠️ Technology Stack

**Backend:** Python 3, Flask, Flask-CORS
**Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6)
**Data:** JSON-based rule engine (no external AI service or internet connection required)

---

## 📂 Project Structure

```text
BMI-Calculator/
│
├── app.py                     # Flask app & API routes
├── requirements.txt           # Python dependencies
├── README.md
│
├── utils/
│   └── bmi.py                 # BMI, calorie, protein & water calculation logic
│
├── data/
│   └── recommendations.json   # Rule-based recommendation dataset
│
├── templates/
│   └── index.html             # Main UI
│
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── images/
```

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/siddarthshinde06/BMI-Calculator.git
cd BMI-Calculator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

### 4. Open in your browser
```
http://127.0.0.1:5000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Renders the main calculator UI |
| `POST` | `/calculate` | Accepts height, weight, age, gender & goal → returns BMI and full health metrics |
| `GET` | `/health-guide` | Returns the full rule-based recommendation dataset |

**Example request to `/calculate`:**
```json
{
  "height": 175,
  "height_unit": "cm",
  "weight": 70,
  "weight_unit": "kg",
  "age": 25,
  "gender": "male",
  "goal": "maintain"
}
```

---

## 📊 Calculations Performed

- Body Mass Index (BMI)
- BMI Category & Health Risk Level
- Healthy Weight Range
- Weight to Gain or Lose
- BMI Prime
- Ponderal Index
- Estimated Daily Calorie Needs
- Daily Protein Requirement
- Daily Water Intake

---

## 🥗 Health Recommendation Engine

The app uses a **rule-based recommendation system** stored locally in `data/recommendations.json`. Based on the calculated BMI category, it provides:

- ✅ Recommended Foods
- 🚫 Foods to Limit
- 🧪 Essential Nutrients
- 🏃 Exercise Suggestions
- 💡 Lifestyle Tips
- 📋 Health Analysis Summary

No internet connection or external AI service is required — everything runs locally.

---

## 📌 Supported BMI Categories

- Severe Underweight
- Underweight
- Normal Weight
- Overweight
- Obesity Class I
- Obesity Class II
- Obesity Class III

---

## 🔮 Roadmap / Future Improvements

- [ ] Visual BMI charts
- [ ] Child & Teen BMI percentile calculator
- [ ] PDF report download
- [ ] Multi-language support
- [ ] Health dashboard with progress tracking
- [ ] Richer data visualizations

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Siddarth Shinde**

- GitHub: [@siddarthshinde06](https://github.com/siddarthshinde06)
- LinkedIn: [siddarth-shinde](https://linkedin.com/in/siddarth-shinde-807937305)

---

⭐ If you found this project useful, consider giving it a **star** on GitHub!