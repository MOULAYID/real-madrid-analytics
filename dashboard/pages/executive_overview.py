"""
Executive Overview Dashboard Page (Page 1)
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dashboard.components.kpi_card import render_kpi_card
from dashboard.utils.styles import PLOTLY_LAYOUT_TEMPLATE, COLOR_GOLD, COLOR_BLUE, COLOR_GREEN

def render_executive_overview(data: dict, cash_flow_data: list, show_forecast: bool):
    """Renders Page 1: Executive Financial Overview."""
    if not data or "kpis" not in data:
        st.info("Loading Executive Overview analytics...")
        return
        
    kpis = data["kpis"]
    breakdown = data.get("financial_score_breakdown", {})
    revenue_trend = data.get("revenue_trend", [])
    profitability_trend = data.get("profitability_trend", [])
    
    if not show_forecast:
        revenue_trend = [r for r in revenue_trend if not r.get("is_forecast")]
        profitability_trend = [p for p in profitability_trend if not p.get("is_forecast")]

    # 1. 8 KPI Cards Grid
    st.markdown("### 📊 Key Performance Indicators")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            "Total Revenue", 
            kpis.get("revenue_total", 0), 
            change=kpis.get("yoy_revenue_growth"), 
            change_label="YoY",
            tooltip="Total Operating Income (Commercial + Broadcasting + Matchday)"
        )
    with c2:
        render_kpi_card(
            "EBITDA", 
            kpis.get("ebitda", 0),
            tooltip="Earnings Before Interest, Tax, Depreciation & Amortization"
        )
    with c3:
        render_kpi_card(
            "Net Profit", 
            kpis.get("net_profit", 0),
            tooltip="Post-tax Net Earnings reported in official annual accounts"
        )
    with c4:
        render_kpi_card(
            "Cash Position", 
            kpis.get("cash", 0),
            tooltip="Liquid cash balance available at year-end"
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        render_kpi_card(
            "Net Debt", 
            kpis.get("net_debt", 0),
            tooltip="Total Financial Debt minus Cash Position (Excludes Long-term Stadium Loan)"
        )
    with c6:
        render_kpi_card(
            "Wage / Revenue Ratio", 
            kpis.get("wage_ratio", 0),
            prefix="",
            suffix="%",
            tooltip="Staff & Player Salaries / Total Revenue (UEFA FFP Cap: < 70%)"
        )
    with c7:
        render_kpi_card(
            "Squad Market Value", 
            kpis.get("squad_market_value", 0),
            tooltip="Combined Transfermarkt market valuation of active squad"
        )
    with c8:
        render_kpi_card(
            "Financial Health Index", 
            kpis.get("financial_health_score", 0),
            prefix="",
            suffix="/100",
            highlight=True,
            tooltip="Composite score based on Revenue Growth, EBITDA margin, Net Debt leverage, Cash reserve & Diversification"
        )

    st.markdown("---")

    # 2. Financial Strength Gauge & Revenue Trajectory Chart
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.markdown(f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-radius: 10px; padding: 1.25rem; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <span style="font-weight: 700; color: #F3F4F6;">🛡️ Financial Strength Score</span>
                <span class="badge badge-gold">{kpis.get('financial_health_score')}/100</span>
            </div>
            
            <div style="margin: 1rem 0; display: flex; flex-direction: column; gap: 0.85rem;">
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #9CA3AF;">
                        <span>Revenue Growth Strength</span>
                        <span>{breakdown.get('revenue_growth', 0)}%</span>
                    </div>
                    <div style="height: 6px; background: #374151; border-radius: 3px; margin-top: 4px; overflow: hidden;">
                        <div style="width: {min(100, max(10, breakdown.get('revenue_growth', 0) * 4))}%; background: #3B82F6; height: 100%;"></div>
                    </div>
                </div>

                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #9CA3AF;">
                        <span>Profitability Margin (EBITDA)</span>
                        <span>{breakdown.get('profitability_margin', 0)}%</span>
                    </div>
                    <div style="height: 6px; background: #374151; border-radius: 3px; margin-top: 4px; overflow: hidden;">
                        <div style="width: {min(100, breakdown.get('profitability_margin', 0) * 3.5)}%; background: #10B981; height: 100%;"></div>
                    </div>
                </div>

                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #9CA3AF;">
                        <span>Net Debt Leverage Factor</span>
                        <span>{breakdown.get('net_debt_factor', 0)}/100</span>
                    </div>
                    <div style="height: 6px; background: #374151; border-radius: 3px; margin-top: 4px; overflow: hidden;">
                        <div style="width: {breakdown.get('net_debt_factor', 0)}%; background: #F59E0B; height: 100%;"></div>
                    </div>
                </div>

                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #9CA3AF;">
                        <span>Commercial Diversification</span>
                        <span>{breakdown.get('commercial_diversification', 0)}%</span>
                    </div>
                    <div style="height: 6px; background: #374151; border-radius: 3px; margin-top: 4px; overflow: hidden;">
                        <div style="width: {breakdown.get('commercial_diversification', 0) * 2}%; background: #8B5CF6; height: 100%;"></div>
                    </div>
                </div>
            </div>

            <div style="padding: 0.85rem; background: #1F2937; border-radius: 8px; font-size: 0.8rem; color: #D1D5DB; margin-top: 1rem;">
                <strong style="color: #10B981;">Executive Verdict:</strong> Real Madrid demonstrates elite financial resilience with low net debt, zero cash-flow risk, and industry-leading revenue generation exceeding €1B.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        df_rev = pd.DataFrame(revenue_trend)
        fig_rev = px.area(
            df_rev, 
            x="season", 
            y="revenue_total",
            title="Revenue Trajectory (10+ Seasons) (€ Millions)",
            labels={"season": "Season", "revenue_total": "Total Revenue (€M)"}
        )
        fig_rev.update_traces(
            line_color=COLOR_BLUE,
            fillcolor="rgba(59, 130, 246, 0.2)"
        )
        fig_rev.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=330)
        st.plotly_chart(fig_rev, use_container_width=True)

    # 3. 3-Statement Cash Flow Decomposition Table
    if cash_flow_data:
        st.markdown("---")
        st.markdown("### 💵 3-Statement Cash Flow Decomposition (€ Millions)")
        df_cf = pd.DataFrame(cash_flow_data)
        
        # Display formatted table using Streamlit dataframe
        formatted_cf = df_cf.copy()
        formatted_cf.columns = [
            "Season", "Operating Cash Flow (€M)", "Investing Cash Flow (€M)", 
            "Financing Cash Flow (€M)", "Net Cash Change (€M)", "Ending Cash Balance (€M)"
        ]
        st.dataframe(formatted_cf, use_container_width=True, hide_index=True)

    # 4. Profitability Evolution Chart
    st.markdown("---")
    df_prof = pd.DataFrame(profitability_trend)
    fig_prof = px.bar(
        df_prof,
        x="season",
        y=["ebitda", "net_profit"],
        barmode="group",
        title="Profitability Evolution (EBITDA vs Net Profit €M)",
        color_discrete_sequence=[COLOR_GOLD, COLOR_GREEN],
        labels={"season": "Season", "value": "€ Millions", "variable": "Metric"}
    )
    fig_prof.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=340)
    st.plotly_chart(fig_prof, use_container_width=True)
