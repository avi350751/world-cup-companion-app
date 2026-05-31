# 🏆 World Cup 2026 Football Companion

A modern interactive web app to explore World Cup 2026 players, analyze team performance, and predict tournament outcomes.


## ✨ Features

### **Tab 1: 🏆 Teams & Data**
- World Cup 2026 showcase with all participating nations
- Teams organized by continent with squad stats
- Load default data or upload custom CSV file

### **Tab 2: 🔍 Player Details**
- Smart player search by country
- View player stats: position, age, club, height, weight
- World Cup record: appearances, goals, assists
- MVP indicator for top performers

### **Tab 3: 📊 Country Analysis**
- Country strength overview with 5 key metrics
- Top 5 players ranked by performance
- Tournament prediction (Knockout stage forecast)
- Squad composition breakdown

---

## 🚀 Quick Start

### **Windows**
```bash
cd wc-football-companion
run.bat
```

### **Mac/Linux**
```bash
cd wc-football-companion
./run.sh
```

### **Using UV**
```bash
uv sync
uv run streamlit run app.py
```

### **Using pip**
```bash
pip install -r requirements.txt
streamlit run app.py
```

App opens at: `http://localhost:8501`

---

## 📊 Data Format

CSV with these columns:
- `Player_Name`, `Country`, `Club`, `Position`, `Age`
- `WC_Appearances`, `WC_Goals`, `WC_Assists`, `IsMVP`
- `Height_cm`, `Weight_kg`, `Weight_lbs`, `Jersey_Number`

**Note:** Height converts from cm to feet-inches (e.g., 183cm → 6-0)

---

## 📁 Project Structure

```
wc-football-companion/
├── app.py                          # Main application
├── pyproject.toml                  # Project config
├── requirements.txt                # Dependencies
|
├── data/
│   └── 2026_FIFA_World_Cup_Players_2.csv
│
└── src/
    ├── constants.py                # Flags, colors, metadata
    ├── data_loader.py              # Data handling
    └── predictions.py              # Prediction engine
```

---

## 🎨 Design

- **Dark Theme:** Professional dark interface with vibrant accents
- **Color Scheme:** Blue (#1f77e3), Orange (#ff6b35), Gold (#ffd60a)
- **Modern UI:** Smooth animations, gradient backgrounds, responsive layout
- **Uniform Tabs:** Equal sizing with 0.3s transitions

---

## 🎯 Prediction Algorithm

Strength Score = (Avg Goals × 25) + (Avg Assists × 15) + (MVPs × 8) + (Squad × 0.2) + (Experience × 3)

**Prediction Stages:**
- **80-100:** 🏆 Strong Contender → Semifinals/Finals
- **65-79:** 🥈 Competitive → Quarterfinals
- **50-64:** ⚡ Mid-tier → Quarterfinals
- **35-49:** 🎯 Challenger → Group Stage
- **<35:** 🌟 Underdog → Early Exit

---

## 📦 Dependencies

- **streamlit** (≥1.28.0) - Web framework
- **pandas** (≥2.0.0) - Data handling
- **plotly** (≥5.14.0) - Charts
- **requests** (≥2.31.0) - HTTP
- **pillow** (≥10.0.0) - Images

---

## 🧪 Testing

### Tab 1 - Teams & Data
- ✅ Load default data
- ✅ Teams display by continent
- ✅ Flag emojis show correctly
- ✅ Squad stats visible

### Tab 2 - Player Finder
- ✅ Country/player selection works
- ✅ All stats display correctly
- ✅ MVP badge shows for MVPs
- ✅ Height converts properly

### Tab 3 - Country Analysis
- ✅ Stats calculated correctly
- ✅ Top 5 players ranked properly
- ✅ Prediction score generates
- ✅ Confidence level displays

---

## 🛠️ Customization

### Change Colors
Edit `src/constants.py`:
```python
SPORT_COLORS = {
    "primary": "#1f77e3",      # Change primary color
    "secondary": "#ff6b35",    # Change secondary color
    # ...
}
```

### Adjust Prediction Weights
Edit `src/predictions.py` `calculate_country_strength()`:
```python
strength_score = (
    (avg_goals_per_player * 25) +      # Adjust weight
    (avg_assists_per_player * 15) +    # Adjust weight
    # ...
)
```

### Add Countries
Edit `src/constants.py` `COUNTRY_FLAGS`:
```python
"New Country": "🇦🇶",  # Add flag emoji
```

---

## 📚 Documentation

For detailed documentation, see:
- `README.md` - This file

---

## 📝 License

Open source for educational and personal use.

---
