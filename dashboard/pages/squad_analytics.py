"""
Squad Investment Analytics Dashboard Page (Page 4)
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.utils.styles import PLOTLY_LAYOUT_TEMPLATE, COLOR_GOLD, COLOR_GREEN, COLOR_RED, COLOR_BLUE

def render_squad_analytics(data: dict):
    """Renders Page 4: Squad Investment Analytics & Player Economics."""
    if not data or "transfer_summary" not in data:
        st.info("Loading Squad Analytics...")
        return
        
    transfer_summary = data["transfer_summary"]
    player_econ = data.get("player_economics", [])
    capital_gains = data.get("capital_gains", [])

    # 1. 10-Season Transfer Expenditure & Net Spend Chart
    st.markdown("### ⚽ Squad Investment & Transfer Strategy")
    df_trans = pd.DataFrame(transfer_summary)
    fig_trans = px.bar(
        df_trans,
        x="season",
        y=["spent", "received", "net_spend"],
        barmode="group",
        title="Transfer Expenditure, Sales & Net Spend per Season (€ Millions)",
        color_discrete_sequence=[COLOR_RED, COLOR_GREEN, COLOR_BLUE],
        labels={"season": "Season", "value": "€ Millions", "variable": "Category"}
    )
    fig_trans.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=330)
    st.plotly_chart(fig_trans, use_container_width=True)

    # 2. Capital Gains on Player Sales (Plusvalías) Section
    if capital_gains:
        st.markdown("---")
        st.markdown("### 📈 Capital Gains on Player Sales (Plusvalías en Traspasos)")
        st.caption("In Spanish GAAP / IFRS football accounting, Net Profit on sales equals **Sale Price minus Unamortized Book Value**.")
        df_cg = pd.DataFrame(capital_gains)
        df_cg.columns = ["Season", "Player Sold", "Sale Price (€M)", "Unamortized Book Value (€M)", "Net Capital Gain (€M)"]
        st.dataframe(df_cg, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 3. Interactive Scatter Plot: Player Cost vs Sporting Contribution Matrix
    st.markdown("### 🎯 Player Cost vs Sporting Contribution Matrix")
    st.caption("High performing, cost-efficient stars populate the top-left quadrant. Bubble size reflects Transfermarkt Market Value (€M).")
    
    df_players = pd.DataFrame(player_econ)
    if not df_players.empty:
        fig_scatter = px.scatter(
            df_players,
            x="salary_estimate",
            y="performance_score",
            size="market_value",
            color="performance_score",
            hover_name="player",
            hover_data={
                "salary_estimate": ":.1fM",
                "market_value": ":.0fM",
                "performance_score": ":.1f",
                "goals": True,
                "assists": True
            },
            color_continuous_scale=[[0, COLOR_RED], [0.5, COLOR_GOLD], [1, COLOR_GREEN]],
            labels={
                "salary_estimate": "Annual Salary (€M)",
                "performance_score": "Performance Score (out of 10)",
                "market_value": "Market Value (€M)"
            },
            title="Player Salary vs Performance Score Matrix"
        )
        fig_scatter.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=380, yaxis_range=[5, 10])
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 4. Player Economics Data Table with Search Filter
    st.markdown("---")
    st.markdown("### 🔍 Active Squad Player Economics Table")
    search_term = st.text_input("Filter player name", value="", placeholder="Search Vinícius, Mbappé, Bellingham...")
    
    if not df_players.empty:
        filtered_df = df_players.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df["player"].str.contains(search_term, case=False, na=False)]
            
        display_df = filtered_df[[
            "player", "season", "salary_estimate", "market_value", 
            "minutes_played", "goals", "assists", "performance_score"
        ]].copy()
        display_df.columns = [
            "Player Name", "Season", "Est. Salary (€M)", "Market Value (€M)", 
            "Minutes Played", "Goals", "Assists", "Performance Score"
        ]
        st.dataframe(display_df, use_container_width=True, hide_index=True)
