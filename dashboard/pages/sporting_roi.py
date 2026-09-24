"""
Sporting ROI Dashboard Page (Page 5)
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from dashboard.components.kpi_card import render_kpi_card
from dashboard.utils.styles import PLOTLY_LAYOUT_TEMPLATE, COLOR_GOLD, COLOR_BLUE, COLOR_GREEN, COLOR_PURPLE

def render_sporting_roi(data: dict):
    """Renders Page 5: Sporting Success vs Financial Power."""
    if not data or "roi_data" not in data:
        st.info("Loading Sporting ROI analytics...")
        return
        
    roi_data = data["roi_data"]
    summary_text = data.get("summary", "")
    
    avg_roi = sum([r["football_roi_score"] for r in roi_data]) / len(roi_data) if roi_data else 0

    # 1. Summary KPI Cards
    st.markdown("### 🏆 Sporting ROI & Silverware Efficiency")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card(
            "Average Football ROI Score",
            round(avg_roi, 1),
            prefix="",
            suffix=" pts / €100M",
            highlight=True,
            tooltip="Success Points (Trophies + UCL + Position) / Financial Investment (€100M Wages + Amortization)"
        )
    with c2:
        render_kpi_card(
            "10-Year Major Trophies",
            24,
            prefix="",
            suffix=" Trophies",
            tooltip="Includes 5 Champions League titles, 4 La Liga titles, Copa del Rey, Club World Cups"
        )
    with c3:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-left: 4px solid #F59E0B; border-radius: 10px; padding: 1rem 1.25rem; height: 100%;">
            <div style="font-size: 0.75rem; font-weight: 600; color: #9CA3AF;">EXECUTIVE STRATEGIC SUMMARY</div>
            <p style="font-size: 0.82rem; color: #F3F4F6; margin-top: 0.4rem; line-height: 1.4;">
                {summary_text}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. Revenue vs Trophies & Wages vs ROI Score Dual-Axis Charts
    c_left, c_right = st.columns(2)
    df_roi = pd.DataFrame(roi_data)
    
    with c_left:
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=df_roi["season"],
            y=df_roi["revenue"],
            name="Total Revenue (€M)",
            marker_color=COLOR_BLUE,
            opacity=0.8
        ))
        fig1.add_trace(go.Scatter(
            x=df_roi["season"],
            y=df_roi["trophies"],
            name="Trophies Won",
            yaxis="y2",
            line=dict(color=COLOR_GOLD, width=3),
            mode="lines+markers"
        ))
        fig1.update_layout(
            title="Revenue vs Trophies Won per Season",
            yaxis=dict(title="Revenue (€M)"),
            yaxis2=dict(title="Trophies", overlaying="y", side="right", range=[0, 6]),
            **PLOTLY_LAYOUT_TEMPLATE,
            height=340
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c_right:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df_roi["season"],
            y=df_roi["wages"],
            name="Wage Bill (€M)",
            marker_color=COLOR_PURPLE,
            opacity=0.8
        ))
        fig2.add_trace(go.Scatter(
            x=df_roi["season"],
            y=df_roi["football_roi_score"],
            name="Football ROI Score",
            yaxis="y2",
            line=dict(color=COLOR_GREEN, width=3),
            mode="lines+markers"
        ))
        fig2.update_layout(
            title="Wages vs Football ROI Score Efficiency",
            yaxis=dict(title="Wage Bill (€M)"),
            yaxis2=dict(title="ROI Score", overlaying="y", side="right"),
            **PLOTLY_LAYOUT_TEMPLATE,
            height=340
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 3. Performance Matrix Table
    st.markdown("---")
    st.markdown("### 📋 Historical Season Sporting & Financial Matrix")
    display_matrix = df_roi[[
        "season", "revenue", "wages", "league_position", 
        "champions_league_result", "trophies", "football_roi_score"
    ]].copy()
    display_matrix.columns = [
        "Season", "Revenue (€M)", "Wage Bill (€M)", "La Liga Position", 
        "Champions League Stage", "Trophies Won", "Football ROI Score"
    ]
    st.dataframe(display_matrix, use_container_width=True, hide_index=True)
