# Forecast-to-Inventory: Demand Forecasting Drives Inventory Decisions

## The Question
Better demand forecasts should mean less inventory at the same service level — but how much less, and is the difference worth the modeling complexity? This project quantifies that tradeoff using Walmart retail sales data.

## Approach
Forecast daily SKU-level demand with multiple methods (naive baseline, ETS, ARIMA, LightGBM), feed each forecast into a reorder-point inventory policy, and simulate the resulting service levels and inventory investment over a 28-day test period.

## Status
🚧 In progress.

## Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Data: M5 Forecasting dataset from Kaggle. See `data/README.md` for download instructions.

What each folder is for:

data/raw/ — the original Kaggle CSVs, never modified
data/processed/ — cleaned/filtered data you create
notebooks/ — Jupyter notebooks for exploration and analysis, one per phase
src/ — reusable Python functions (metrics, models, simulation logic)
results/figures/ — saved plots
dashboard/ — the Streamlit app, later

