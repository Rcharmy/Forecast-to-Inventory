"""Forecast-to-Inventory Dashboard — main app entry point."""
import streamlit as st
import sys
from pathlib import Path

# Make sibling modules importable
sys.path.insert(0, str(Path(__file__).parent))

from styling import CUSTOM_CSS
import pages_money
import pages_sku
import pages_pattern


st.set_page_config(
    page_title="Forecast-to-Inventory | Demand forecasting drives inventory decisions",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# 📦 Forecast → Inventory")
    st.markdown("*A simulation of how forecast accuracy drives inventory decisions in retail*")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        options=[
            "💰 The money chart",
            "🔍 SKU explorer",
            "📊 Pattern deep dive"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Project context")
    st.markdown("""
    **Data:** Walmart M5 — FOODS category, store CA_1
    **Scope:** 1,437 SKUs, 1,941 days of history
    **Lead time:** 7 days
    **Test period:** 28 days
    """)

    st.markdown("---")
    st.markdown("### Built by")
    st.markdown("Charmy Raj")
    st.markdown("[GitHub repo](https://github.com/Rcharmy/Forecast-to-Inventory)")


# Main content
if page.startswith("💰"):
    pages_money.render()
elif page.startswith("🔍"):
    pages_sku.render()
elif page.startswith("📊"):
    pages_pattern.render()


# Footer
st.markdown(
    '<div class="footer">Forecast-to-Inventory simulation | '
    'Built with Python, pandas, statsmodels, LightGBM, and Streamlit</div>',
    unsafe_allow_html=True
)