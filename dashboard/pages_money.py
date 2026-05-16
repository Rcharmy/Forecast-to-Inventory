"""Tab 1: The headline money chart with interactive service-level selection."""
import streamlit as st
import plotly.graph_objects as go
from data_loader import load_portfolio_results
from styling import render_headline_card


def render():
    portfolio = load_portfolio_results()

    st.markdown("## How much inventory can better forecasts save?")
    st.markdown(
        "The chart below shows total average inventory investment against achieved "
        "fill rate for two forecasting policies. The gap between the two curves is "
        "the **working capital that better forecasts free up at the same service level**."
    )

    # Service level slider
    available_sls = sorted(portfolio["service_level"].unique())
    selected_sl = st.select_slider(
        "Target service level",
        options=available_sls,
        value=0.95,
        format_func=lambda x: f"{x*100:.0f}%"
    )

    # Get the numbers at the selected service level
    at_sl = portfolio[portfolio["service_level"] == selected_sl]
    inv_naive = at_sl[at_sl["model"] == "naive"]["total_inventory_dollars"].values[0]
    inv_ets = at_sl[at_sl["model"] == "ets"]["total_inventory_dollars"].values[0]
    fill_naive = at_sl[at_sl["model"] == "naive"]["weighted_fill_rate"].values[0]
    fill_ets = at_sl[at_sl["model"] == "ets"]["weighted_fill_rate"].values[0]
    savings = inv_naive - inv_ets
    savings_pct = (savings / inv_naive) * 100

    # Top row: three big headline cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            render_headline_card(
                "Naive policy inventory",
                f"${inv_naive:,.0f}",
                f"Achieves {fill_naive*100:.1f}% fill rate"
            ), unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            render_headline_card(
                "ETS policy inventory",
                f"${inv_ets:,.0f}",
                f"Achieves {fill_ets*100:.1f}% fill rate"
            ), unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            render_headline_card(
                "Inventory savings",
                f"${savings:,.0f}",
                f"{savings_pct:.1f}% reduction at {selected_sl*100:.0f}% target SL"
            ), unsafe_allow_html=True
        )

    # The money chart
    fig = go.Figure()

    for model, name, color, dash in [
        ("naive", "Seasonal Naive (baseline)", "#9ca3af", "dash"),
        ("ets", "ETS (improved forecast)", "#2d6a4f", "solid")
    ]:
        sub = portfolio[portfolio["model"] == model].sort_values("weighted_fill_rate")
        fig.add_trace(go.Scatter(
            x=sub["weighted_fill_rate"] * 100,
            y=sub["total_inventory_dollars"],
            mode="lines+markers",
            name=name,
            line=dict(color=color, width=3, dash=dash),
            marker=dict(size=10, color=color, line=dict(color="white", width=1.5)),
            hovertemplate="<b>%{fullData.name}</b><br>Fill rate: %{x:.1f}%<br>Inventory: $%{y:,.0f}<extra></extra>"
        ))

    # Highlight the selected service level
    fig.add_trace(go.Scatter(
        x=[fill_naive*100, fill_ets*100],
        y=[inv_naive, inv_ets],
        mode="markers",
        marker=dict(size=18, color="orange", symbol="star",
                    line=dict(color="white", width=2)),
        name=f"At {selected_sl*100:.0f}% target",
        hovertemplate="<b>Selected point</b><br>%{x:.1f}% fill rate<br>$%{y:,.0f} inventory<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="Inventory investment vs achieved fill rate",
            font=dict(size=18)
        ),
        xaxis=dict(title="Achieved fill rate (%)", gridcolor="#e5e7eb"),
        yaxis=dict(title="Total average inventory ($)", gridcolor="#e5e7eb",
                   tickformat="$,.0f"),
        height=480,
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="closest"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Narrative below
    st.markdown("### What this shows")
    st.markdown(f"""
    Forecast error standard deviation dropped by **29% on average per SKU** when switching
    from seasonal-naive to ETS forecasts. Because safety stock scales directly with σ
    (safety stock = z × σ × √lead time), lower forecast error means lower safety stock
    can sustain the same service level — which is the gap visible between the two curves.

    At a **{selected_sl*100:.0f}% target service level**, ETS-based replenishment policies
    require **${savings:,.0f} less average inventory** ({savings_pct:.1f}% reduction) than
    naive-based policies across the simulated catalog of 1,437 SKUs over 28 days.

    **What's *not* shown — and why this matters:** total inventory is the sum of cycle
    stock (set by order quantity) and safety stock (set by forecast error). Only safety
    stock responds to forecast quality. The percentage savings here reflect that cycle
    stock dominates total inventory under a 4-week order cycle. Tighter order cycles or
    higher-value SKUs would amplify the percentage benefit.
    """)