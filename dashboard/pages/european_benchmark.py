"""
European Benchmark Dashboard Page (Page 7)
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.utils.styles import PLOTLY_LAYOUT_TEMPLATE, COLOR_GOLD, COLOR_BLUE, COLOR_GREEN, COLOR_RED, COLOR_PURPLE, COLOR_PINK

CLUB_COLORS = {
    "Real Madrid": COLOR_GOLD,
    "Manchester City": COLOR_BLUE,
    "Paris Saint-Germain": COLOR_PURPLE,
    "FC Barcelona": COLOR_PINK,
    "Bayern Munich": COLOR_RED,
    "Liverpool FC": COLOR_GREEN
}

def render_european_benchmark(data: dict):
    """Renders Page 7: European Elite Club Benchmarking."""
    if not data or "clubs" not in data:
        st.info("Loading European Benchmark analytics...")
        return
        
    clubs = data["clubs"]
    matrix = data.get("positioning_matrix", [])

    # 1. Competitive Positioning Matrix Scatter Plot
    st.markdown("### 🌍 European Elite Competitive Positioning Matrix")
    st.caption("Top-right quadrant represents absolute football dominance (High Financial Resilience + Elite Silverware Output).")
    
    df_matrix = pd.DataFrame(matrix)
    if not df_matrix.empty:
        fig_scatter = px.scatter(
            df_matrix,
            x="financial_power",
            y="sporting_success",
            size="revenue",
            color="club",
            hover_name="club",
            hover_data={
                "financial_power": True,
                "sporting_success": True,
                "revenue": ":.0fM",
                "wage_ratio": ":.1f%",
                "squad_value": ":.0fM",
                "trophies": True
            },
            color_discrete_map=CLUB_COLORS,
            labels={
                "financial_power": "Financial Power Index (0-100)",
                "sporting_success": "Sporting Success Index (0-100)",
                "revenue": "Revenue (€M)"
            },
            title="Financial Power vs Sporting Success Matrix"
        )
        fig_scatter.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=380, xaxis_range=[60, 100], yaxis_range=[60, 100])
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # 2. Side-by-Side Deloitte Money League Revenue Stacked Bar Chart
    st.markdown("### 💶 Deloitte Money League Revenue Streams Comparison (€ Millions)")
    df_clubs = pd.DataFrame(clubs)
    fig_bar = px.bar(
        df_clubs,
        x="club",
        y=["commercial_revenue", "broadcasting_revenue", "matchday_revenue"],
        title="Revenue Stream Breakdown by Peer Club (€M)",
        color_discrete_sequence=[COLOR_GOLD, COLOR_BLUE, COLOR_GREEN],
        labels={"club": "Club Name", "value": "Revenue (€M)", "variable": "Stream"}
    )
    fig_bar.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=340)
    st.plotly_chart(fig_bar, use_container_width=True)

    # 3. Multi-Club Comprehensive Data Table
    st.markdown("---")
    st.markdown("### 📊 Elite European Peer Group Financial & Sporting Benchmark Table")
    
    display_clubs = df_clubs[[
        "club", "revenue", "commercial_revenue", "wage_ratio", 
        "net_debt", "squad_value", "five_yr_net_transfer_spend", "five_yr_trophies"
    ]].copy()
    display_clubs.columns = [
        "Club Name", "Total Revenue (€M)", "Commercial Revenue (€M)", "Wage Ratio (%)", 
        "Net Debt (€M)", "Squad Value (€M)", "5-Yr Net Spend (€M)", "5-Yr Trophies"
    ]
    st.dataframe(display_clubs, use_container_width=True, hide_index=True)
