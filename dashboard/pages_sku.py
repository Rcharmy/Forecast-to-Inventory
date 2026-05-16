"""Tab 2: Drill into individual SKUs — forecasts, actuals, inventory trajectory."""
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_loader import load_forecasts, load_sales_history, load_sku_metadata


def render():
    forecasts = load_forecasts()
    sales = load_sales_history()
    skus_meta = load_sku_metadata()

    st.markdown("## Drill into individual SKUs")
    st.markdown(
        "Pick a SKU to see its historical demand pattern, the test-period forecasts "
        "from each model, and per-SKU forecast accuracy."
    )

    # SKU selector — filter by pattern first to make it manageable
    col1, col2 = st.columns([1, 2])
    with col1:
        pattern_filter = st.selectbox(
            "Demand pattern",
            options=["smooth", "erratic", "lumpy", "intermittent"],
            index=0,
            help="Pre-filter SKUs by their demand pattern classification"
        )
    with col2:
        eligible_skus = skus_meta[skus_meta["pattern"] == pattern_filter]["id"].sort_values().tolist()
        if not eligible_skus:
            st.warning(f"No SKUs in pattern '{pattern_filter}'.")
            return
        selected_sku = st.selectbox("SKU", options=eligible_skus, index=0)

    # Pull data for this SKU
    sku_history = sales[sales["id"] == selected_sku].sort_values("date")
    sku_forecast = forecasts[forecasts["id"] == selected_sku].sort_values("date")
    sku_meta = skus_meta[skus_meta["id"] == selected_sku].iloc[0]

    # SKU summary metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Avg daily demand", f"{sku_meta['mean_daily']:.2f} units")
    c2.metric("% zero-sales days", f"{sku_meta['pct_zero_days']:.0f}%")
    c3.metric("Pattern", sku_meta["pattern"].capitalize())
    c4.metric("Coefficient of variation", f"{sku_meta['cv']:.2f}")

    # Compute per-SKU forecast accuracy on the test period
    sku_eval = sku_forecast.copy()
    sku_eval["err_naive"] = sku_eval["naive"] - sku_eval["actual"]
    sku_eval["err_ets"] = sku_eval["ets"] - sku_eval["actual"]

    def wmape_local(actual, forecast):
        denom = abs(actual).sum()
        return 100 * abs(actual - forecast).sum() / denom if denom > 0 else float("nan")

    wmape_naive = wmape_local(sku_eval["actual"], sku_eval["naive"])
    wmape_ets = wmape_local(sku_eval["actual"], sku_eval["ets"])

    st.markdown(f"**Test-period forecast accuracy on this SKU:**")
    a1, a2 = st.columns(2)
    a1.metric("Naive WMAPE", f"{wmape_naive:.1f}%")
    a2.metric("ETS WMAPE", f"{wmape_ets:.1f}%",
              delta=f"{wmape_ets - wmape_naive:+.1f} pp vs naive",
              delta_color="inverse")

    # Historical demand chart with forecast period overlaid
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.55, 0.45],
        shared_xaxes=False,
        subplot_titles=("Full historical demand", "Test-period forecasts vs actuals"),
        vertical_spacing=0.15
    )

    # Top: full history
    fig.add_trace(
        go.Scatter(
            x=sku_history["date"], y=sku_history["units_sold"],
            mode="lines", name="Historical demand",
            line=dict(color="#374151", width=1)
        ),
        row=1, col=1
    )

    # Highlight test period
    if len(sku_forecast) > 0:
        test_start = sku_forecast["date"].min()
        test_end = sku_forecast["date"].max()
        fig.add_vrect(
            x0=test_start, x1=test_end,
            fillcolor="orange", opacity=0.15, line_width=0,
            row=1, col=1
        )

    # Bottom: test period actuals and forecasts
    fig.add_trace(
        go.Scatter(
            x=sku_forecast["date"], y=sku_forecast["actual"],
            mode="lines+markers", name="Actual",
            line=dict(color="black", width=2),
            marker=dict(size=6)
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=sku_forecast["date"], y=sku_forecast["naive"],
            mode="lines+markers", name="Naive forecast",
            line=dict(color="#9ca3af", width=2, dash="dash"),
            marker=dict(size=5)
        ),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=sku_forecast["date"], y=sku_forecast["ets"],
            mode="lines+markers", name="ETS forecast",
            line=dict(color="#2d6a4f", width=2),
            marker=dict(size=5)
        ),
        row=2, col=1
    )

    fig.update_layout(
        height=620,
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="left", x=0),
        margin=dict(t=70, b=40)
    )
    fig.update_xaxes(gridcolor="#e5e7eb")
    fig.update_yaxes(gridcolor="#e5e7eb", title="Units sold")

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Top: full historical sales for this SKU. Orange shading marks the 28-day "
        "test window. Bottom: zoomed into the test window with actuals and both "
        "model forecasts."
    )