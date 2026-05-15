"""Forecast accuracy metrics for supply chain forecasting."""
import numpy as np
import pandas as pd


def wmape(actual: np.ndarray, forecast: np.ndarray) -> float:
    """
    Weighted MAPE — the standard accuracy metric in retail forecasting.
    Weighted by volume so high-selling SKUs count more than slow movers.
    Returns a percentage (0-100+).
    """
    actual = np.asarray(actual)
    forecast = np.asarray(forecast)
    denom = np.sum(np.abs(actual))
    if denom == 0:
        return np.nan
    return 100.0 * np.sum(np.abs(actual - forecast)) / denom


def bias(actual: np.ndarray, forecast: np.ndarray) -> float:
    """
    Mean forecast error: positive = over-forecasting, negative = under-forecasting.
    Bias matters enormously in supply chain — persistent over-forecasting
    inflates inventory; persistent under-forecasting causes stockouts.
    Returns same units as the actuals (e.g., units/day).
    """
    return float(np.mean(np.asarray(forecast) - np.asarray(actual)))


def rmse(actual: np.ndarray, forecast: np.ndarray) -> float:
    """Root mean squared error — penalizes large errors more than small ones."""
    actual = np.asarray(actual)
    forecast = np.asarray(forecast)
    return float(np.sqrt(np.mean((actual - forecast) ** 2)))


def evaluate_forecasts(df: pd.DataFrame,
                       actual_col: str = "actual",
                       forecast_col: str = "forecast",
                       group_cols: list = None) -> pd.DataFrame:
    """
    Compute WMAPE, bias, and RMSE either overall or by group.
    df must have columns [actual, forecast, ...optional group cols].
    """
    if group_cols is None:
        return pd.DataFrame([{
            "wmape": wmape(df[actual_col], df[forecast_col]),
            "bias": bias(df[actual_col], df[forecast_col]),
            "rmse": rmse(df[actual_col], df[forecast_col]),
            "n_obs": len(df)
        }])

    rows = []
    for keys, sub in df.groupby(group_cols):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(group_cols, keys))
        row.update({
            "wmape": wmape(sub[actual_col], sub[forecast_col]),
            "bias": bias(sub[actual_col], sub[forecast_col]),
            "rmse": rmse(sub[actual_col], sub[forecast_col]),
            "n_obs": len(sub)
        })
        rows.append(row)
    return pd.DataFrame(rows)