# Mettur Dam Daily Update

This project provides **daily updates of Mettur Dam (Stanley Reservoir)** using real data from the **Tamil Nadu Government Reservoirs website**.  
The data is automatically updated using **GitHub Actions** and served publicly via **GitHub Pages**.

---

## 📊 Features

- Fetches **real-time Mettur Dam data** daily:
  - Water level (ft)
  - Storage (MCft)
  - Inflow (Cusecs)
  - Outflow (Cusecs)
- Calculates **daily changes** compared to the previous day:
  - `water_level_change_ft`
  - `inflow_change_cusecs`
  - `outflow_change_cusecs`
- Updates `daily.json` automatically in the repository
- Publicly available for apps or services to consume

---

## 🌐 Live URL

After enabling GitHub Pages, the daily JSON can be accessed at:

```
https://asma1611.github.io/mettur-dam/daily.json
```

---

## 🛠 How It Works

1. **GitHub Actions** workflow runs every day at 6 AM UTC.
2. Fetches the latest Mettur Dam data from the official site:
   [Tamil Nadu Reservoirs](https://tnagriculture.in/ARS/home/reservoir)
3. Compares with the previous day's data and calculates differences.
4. Updates `daily.json` and pushes it to GitHub automatically.

---

## 📁 Project Structure

```
mettur-dam/
│
├── daily.json             # Daily Mettur Dam data
├── README.md              # Project explanation
└── .github/
    └── workflows/
        └── update-mettur-dam.yml   # GitHub Actions workflow
```

---

## 🔐 Notes

- No authentication is required for apps to access `daily.json`.
- The workflow commits daily updates automatically.
- The project is beginner-friendly and demonstrates **real-time data updates using GitHub Actions**.

---

## 📈 Example Output (`daily.json`)

```json
{
  "dam_name": "Mettur Dam (Stanley Reservoir)",
  "date": "2026-01-10",
  "water_level_ft": 99.80,
  "storage_mcft": 64500,
  "inflow_cusecs": 210,
  "outflow_cusecs": 7600,
  "water_level_change_ft": +0.45,
  "inflow_change_cusecs": -15,
  "outflow_change_cusecs": +280,
  "source": "https://tnagriculture.in/ARS/home/reservoir"
}
```

---

## 📌 How to Use

1. Fetch the JSON in your app or service:

```javascript
fetch('https://asma1611.github.io/mettur-dam/daily.json')
  .then(res => res.json())
  .then(data => console.log(data));
```

2. Use the fields for **displaying daily dam updates** or analytics.

---

## 👩‍💻 Author

- GitHub: [asma1611](https://github.com/asma1611)
- Project: Beginner-friendly GitHub Actions + GitHub Pages example
