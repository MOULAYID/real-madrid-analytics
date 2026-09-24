"""
Reusable KPI Card Renderer Component for Streamlit Dashboard.
"""
import streamlit as st

def render_kpi_card(
    title: str,
    value: float | int | str,
    change: float | None = None,
    change_label: str = "YoY",
    prefix: str = "€",
    suffix: str = "M",
    highlight: bool = False,
    tooltip: str | None = None
):
    """Renders a styled executive KPI card."""
    card_class = "kpi-card kpi-card-highlight" if highlight else "kpi-card"
    
    # Format value
    if isinstance(value, float):
        formatted_val = f"{prefix}{value:,.1f}{suffix}" if suffix != "%" else f"{prefix}{value:.1f}%"
    elif isinstance(value, int):
        formatted_val = f"{prefix}{value:,}{suffix}"
    else:
        formatted_val = f"{prefix}{value}{suffix}"
        
    change_html = ""
    if change is not None:
        sign = "+" if change > 0 else ""
        change_class = "kpi-change-positive" if change >= 0 else "kpi-change-negative"
        change_html = f'<span class="{change_class}">{sign}{change}% {change_label}</span>'
        
    tooltip_html = f'<div class="kpi-tooltip">{tooltip}</div>' if tooltip else ""

    card_html = f"""
    <div class="{card_class}">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value-container">
            <span class="kpi-value">{formatted_val}</span>
            {change_html}
        </div>
        {tooltip_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
