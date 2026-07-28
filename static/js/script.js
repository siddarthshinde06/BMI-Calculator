// ============ Unit system toggle ============
const unitButtons = document.querySelectorAll(".unit-btn");
let currentSystem = "metric";

unitButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    unitButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentSystem = btn.dataset.system;
    toggleUnitRows();
  });
});

function toggleUnitRows() {
  const metricOn = currentSystem === "metric";
  document.getElementById("heightMetricRow").classList.toggle("hidden", !metricOn);
  document.getElementById("heightImperialRow").classList.toggle("hidden", metricOn);
  document.getElementById("weightMetricRow").classList.toggle("hidden", !metricOn);
  document.getElementById("weightImperialRow").classList.toggle("hidden", metricOn);
  document.getElementById("stonePoundsRow").classList.add("hidden"); // shown only if stone chosen
}

// Show stone+lb row when "stone" is selected
document.getElementById("weightUnitImperial").addEventListener("change", (e) => {
  const isStone = e.target.value === "stone";
  document.getElementById("stonePoundsRow").classList.toggle("hidden", !isStone);
  document.getElementById("weightImperialRow").classList.toggle("hidden", isStone);
});

// ============ Dark mode ============
const themeToggle = document.getElementById("themeToggle");
themeToggle.addEventListener("click", () => {
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  document.documentElement.setAttribute("data-theme", isDark ? "light" : "dark");
  themeToggle.textContent = isDark ? "🌙 Dark Mode" : "☀️ Light Mode";
});

// ============ Form submit ============
const form = document.getElementById("bmiForm");
const errorBox = document.getElementById("errorBox");
const resultCard = document.getElementById("resultCard");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideError();

  const payload = buildPayload();
  if (!payload) return; // validation failed client-side

  try {
    const res = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (!res.ok) {
      showError(data.error || "Something went wrong. Please check your inputs.");
      return;
    }

    renderResults(data);
    saveToRecent(data);
  } catch (err) {
    showError("Could not reach the server. Please make sure app.py is running.");
  }
});

function buildPayload() {
  let height, height_unit, weight, weight_unit;

  if (currentSystem === "metric") {
    height = parseFloat(document.getElementById("heightCm").value);
    height_unit = document.getElementById("heightUnitMetric").value;

    const weightUnit = document.getElementById("weightUnitMetric").value;
    weight = parseFloat(document.getElementById("weightKg").value);
    weight_unit = weightUnit;
  } else {
    const ft = parseFloat(document.getElementById("heightFt").value) || 0;
    const inch = parseFloat(document.getElementById("heightIn").value) || 0;
    height = ft * 12 + inch; // total inches
    height_unit = "inches";

    const stoneMode = document.getElementById("weightUnitImperial").value === "stone";
    if (stoneMode) {
      const stone = parseFloat(document.getElementById("weightStone").value) || 0;
      const lb = parseFloat(document.getElementById("weightStoneLb").value) || 0;
      weight = stone * 14 + lb; // total pounds
      weight_unit = "stone";
    } else {
      weight = parseFloat(document.getElementById("weightLb").value);
      weight_unit = "lb";
    }
  }

  if (!height || height <= 0 || isNaN(height)) {
    showError("Please enter a valid height.");
    return null;
  }
  if (!weight || weight <= 0 || isNaN(weight)) {
    showError("Please enter a valid weight.");
    return null;
  }

  return {
    height, height_unit, weight, weight_unit,
    age: document.getElementById("age").value || null,
    gender: document.getElementById("gender").value || null,
    goal: document.getElementById("goal").value || null
  };
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
}
function hideError() {
  errorBox.classList.add("hidden");
}

// ============ Render results ============
function renderResults(data) {
  resultCard.classList.remove("hidden");

  document.getElementById("bmiScore").textContent = data.bmi;
  document.getElementById("bmiCategory").textContent = data.category;
  document.getElementById("riskLevel").textContent = data.risk_level;
  document.getElementById("healthyRange").textContent =
    `${data.healthy_weight_range.low} - ${data.healthy_weight_range.high} kg`;

  const goal = data.weight_goal;
  document.getElementById("weightGoal").textContent =
    goal.direction === "maintain" ? "Already in range" : `${goal.amount} kg to ${goal.direction}`;

  document.getElementById("bmiPrime").textContent = data.bmi_prime;
  document.getElementById("ponderalIndex").textContent = data.ponderal_index;
  document.getElementById("calories").textContent = `${data.daily_calories} kcal`;
  document.getElementById("protein").textContent = `${data.daily_protein_g} g`;
  document.getElementById("water").textContent = `${data.daily_water_l} L`;

  // Move the meter indicator: scale BMI 10-45 across 0-100%
  const pct = Math.min(100, Math.max(0, ((data.bmi - 10) / (45 - 10)) * 100));
  document.getElementById("meterIndicator").style.left = `calc(${pct}% - 7px)`;

  // Recommendation
  const rec = data.recommendation || {};
  document.getElementById("recAnalysis").textContent = rec.analysis || "";
  fillList("recEat", rec.eat);
  fillList("recLimit", rec.limit);
  fillList("recNutrients", rec.nutrients);
  fillList("recExercise", rec.exercise);
  fillList("recTips", rec.tips);

  resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

function fillList(id, items) {
  const ul = document.getElementById(id);
  ul.innerHTML = "";
  (items || []).forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    ul.appendChild(li);
  });
}

// ============ Reset ============
document.getElementById("resetBtn").addEventListener("click", () => {
  form.reset();
  resultCard.classList.add("hidden");
  hideError();
  document.getElementById("stonePoundsRow").classList.add("hidden");
  toggleUnitRows();
});

// ============ Print ============
document.getElementById("printBtn").addEventListener("click", () => window.print());

// ============ Recent calculations (Local Storage) ============
const recentCard = document.getElementById("recentCard");
const recentList = document.getElementById("recentList");

function saveToRecent(data) {
  const entry = {
    bmi: data.bmi,
    category: data.category,
    time: new Date().toLocaleString()
  };
  const history = JSON.parse(localStorage.getItem("bmiHistory") || "[]");
  history.unshift(entry);
  localStorage.setItem("bmiHistory", JSON.stringify(history.slice(0, 5)));
  renderRecent();
}

function renderRecent() {
  const history = JSON.parse(localStorage.getItem("bmiHistory") || "[]");
  if (history.length === 0) return;
  recentCard.classList.remove("hidden");
  recentList.innerHTML = "";
  history.forEach(item => {
    const li = document.createElement("li");
    li.innerHTML = `<span>${item.time}</span><span>BMI ${item.bmi} — ${item.category}</span>`;
    recentList.appendChild(li);
  });
}

// Init
toggleUnitRows();
renderRecent();
