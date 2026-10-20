"""
Real Madrid Financial Intelligence Dashboard - Main Application Entry Point
Pure Python Executive Dashboard built with Streamlit & Plotly.
"""
import streamlit as st
from dashboard.utils.styles import apply_custom_styles
from dashboard.components.header import render_header
from dashboard.utils.api_client import (
    fetch_overview, fetch_revenue, fetch_costs, fetch_squad,
    fetch_sporting_roi, fetch_stadium, fetch_benchmark,
    fetch_cash_flow, fetch_stress_testing, fetch_esg
)
from dashboard.pages.executive_overview import render_executive_overview
from dashboard.pages.revenue_engine import render_revenue_engine
from dashboard.pages.cost_efficiency import render_cost_efficiency
from dashboard.pages.squad_analytics import render_squad_analytics
from dashboard.pages.sporting_roi import render_sporting_roi
from dashboard.pages.bernabeu_impact import render_bernabeu_impact
from dashboard.pages.european_benchmark import render_european_benchmark
from dashboard.pages.esg_femenino import render_esg_femenino

# Page Configuration
st.set_page_config(
    page_title="Real Madrid CF - Financial Intelligence Platform",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="auto"
)

def main():
    # Apply Custom Executive Theme
    apply_custom_styles()

    # Render Header & Sidebar Controls
    selected_season, show_forecast = render_header()

    # Fetch Data
    overview_data = fetch_overview(season=selected_season)
    revenue_data = fetch_revenue()
    cost_data = fetch_costs()
    squad_data = fetch_squad()
    sporting_roi_data = fetch_sporting_roi()
    stadium_data = fetch_stadium()
    benchmark_data = fetch_benchmark()
    cash_flow_data = fetch_cash_flow()
    stress_data = fetch_stress_testing()
    esg_data = fetch_esg()

    # Create Navigation Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Executive Overview",
        "💰 Revenue Engine",
        "📉 Cost Efficiency",
        "⚽ Squad Analytics",
        "🏆 Sporting ROI",
        "🏟️ Bernabéu & Risk",
        "🌍 European Benchmark",
        "🌱 ESG & Femenino"
    ])

    with tab1:
        render_executive_overview(overview_data, cash_flow_data, show_forecast)

    with tab2:
        render_revenue_engine(revenue_data, show_forecast)

    with tab3:
        render_cost_efficiency(cost_data)

    with tab4:
        render_squad_analytics(squad_data)

    with tab5:
        render_sporting_roi(sporting_roi_data)

    with tab6:
        render_bernabeu_impact(stadium_data, stress_data)

    with tab7:
        render_european_benchmark(benchmark_data)

    with tab8:
        render_esg_femenino(esg_data)

if __name__ == "__main__":
    main()
