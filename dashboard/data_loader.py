"""Data loading for the dashboard, with Streamlit caching for speed."""
import pandas as pd
import streamlit as st
from pathlib import Path

# Paths are relative to where streamlit is run (project root)
PROCESSED_DIR = Path("data") / "processed"
RESULTS_DIR = Path("results")


@st.cache_data
def load_forecasts():
    """Test-period forecasts with actuals and predictions per model."""
    df = pd.read_parquet(PROCESSED_DIR / "forecasts.parquet")
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data
def load_sales_history():
    """Cleaned sales history for the SKU explorer."""
    df = pd.read_parquet(PROCESSED_DIR / "sales_clean.parquet")
    df["date"] = pd.to_datetime(df["date"])
    return df


@st.cache_data
def load_sku_metadata():
    """SKU stats and pattern classification."""
    return pd.read_parquet(PROCESSED_DIR / "modeling_skus.parquet")


@st.cache_data
def load_portfolio_results():
    """Portfolio-level simulation results (the money chart data)."""
    return pd.read_csv(RESULTS_DIR / "portfolio_results.csv")