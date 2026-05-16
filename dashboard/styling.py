"""Custom CSS to make the dashboard look polished rather than default-Streamlit."""

CUSTOM_CSS = """
<style>
    /* Reduce top padding so content sits closer to the top */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Headline metric cards */
    .headline-card {
        background: linear-gradient(135deg, #1f4e3d 0%, #2d6a4f 100%);
        padding: 24px 28px;
        border-radius: 12px;
        color: white;
        margin-bottom: 12px;
    }
    .headline-card .label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        opacity: 0.85;
        margin-bottom: 6px;
    }
    .headline-card .value {
        font-size: 36px;
        font-weight: 700;
        line-height: 1.1;
        margin-bottom: 4px;
    }
    .headline-card .detail {
        font-size: 13px;
        opacity: 0.85;
    }

    /* Section headers */
    h2 {
        margin-top: 1.5rem !important;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 8px;
    }

    /* Smaller, cleaner sidebar */
    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    /* Footer */
    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
        font-size: 12px;
        color: #6b7280;
    }
</style>
"""


def render_headline_card(label: str, value: str, detail: str = "") -> str:
    """Returns HTML for a styled headline metric card."""
    return f"""
    <div class="headline-card">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        <div class="detail">{detail}</div>
    </div>
    """