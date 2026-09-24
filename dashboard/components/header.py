"""
Header and Global Controls Component for Streamlit Dashboard.
"""
import streamlit as st
import pandas as pd
from dashboard.utils.api_client import fetch_trends, load_local_json

SEASONS = [
    "2014/15", "2015/16", "2016/17", "2017/18", "2018/19", 
    "2019/20", "2020/21", "2021/22", "2022/23", "2023/24", "2024/25"
]

def render_header():
    """Renders the executive header and global control widgets in sidebar."""
    st.markdown("""
    <div class="rm-header">
        <div class="rm-title-group">
            <span style="font-size: 2.2rem;">👑</span>
            <div>
                <h1 class="rm-title">REAL MADRID CF</h1>
                <div class="rm-subtitle">Executive Financial Intelligence & Strategic Valuation Platform</div>
            </div>
        </div>
        <div>
            <span class="badge badge-gold">10-Season Analytics</span>
            <span class="badge badge-blue">ML 3-Yr Forecast</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Global Controls in Sidebar
    st.sidebar.markdown("### ⚙️ Executive Controls")
    
    selected_season = st.sidebar.selectbox(
        "Select Active Season",
        options=SEASONS,
        index=10, # Default to 2024/25
        key="season_selector"
    )
    
    show_forecast = st.sidebar.checkbox(
        "Show ML 3-Season Forecasts (2025-2028)",
        value=True,
        key="forecast_toggle"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Data Export")
    
    financials = load_local_json("financials_forecast.json") or []
    if financials:
        df_export = pd.DataFrame(financials)
        csv_data = df_export.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            label="Download Financials (CSV)",
            data=csv_data,
            file_name=f"real_madrid_financials_{selected_season.replace('/', '_')}.csv",
            mime="text/csv"
        )

    # Render Sidebar Trend Alerts Drawer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔔 Executive Trend Alerts")
    trends = fetch_trends()
    if isinstance(trends, list):
        for alert in trends:
            severity_badge = "badge-red" if alert.get("severity") == "high" else "badge-gold" if alert.get("severity") == "medium" else "badge-blue"
            with st.sidebar.expander(f"{alert.get('title', 'Alert')}"):
                st.markdown(f"<span class='badge {severity_badge}'>{alert.get('severity', 'info').upper()}</span>", unsafe_allow_html=True)
                st.markdown(f"**Metric:** `{alert.get('metric', '')}`")
                st.markdown(f"**Observation:** {alert.get('description', '')}")
                st.markdown(f"**Strategic Impact:** {alert.get('impact', '')}")
                
    return selected_season, show_forecast
