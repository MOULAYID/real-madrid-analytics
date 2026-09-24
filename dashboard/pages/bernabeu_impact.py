"""
Santiago Bernabéu Impact & Downside Risk Dashboard Page (Page 6)
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.components.kpi_card import render_kpi_card
from dashboard.utils.styles import PLOTLY_LAYOUT_TEMPLATE, COLOR_GOLD, COLOR_BLUE, COLOR_GREEN, COLOR_RED, COLOR_PURPLE, COLOR_PINK

def render_bernabeu_impact(stadium_data: dict, stress_data: dict):
    """Renders Page 6: Santiago Bernabéu & Downside Risk."""
    if not stadium_data or "scenarios" not in stadium_data:
        st.info("Loading Bernabéu Impact & Risk analytics...")
        return
        
    investment_total = stadium_data.get("investment_total", 1175.0)
    debt_service = stadium_data.get("annual_debt_service", 66.0)
    scenarios = stadium_data.get("scenarios", [])

    # 1. Interactive Scenario Selector
    st.markdown("### 🏟️ Santiago Bernabéu Business Model Scenario Simulator")
    selected_sc_name = st.radio(
        "Select Renovation Projection Scenario:",
        options=[sc["name"] for sc in scenarios],
        index=1,
        horizontal=True
    )
    
    current_scenario = next((sc for sc in scenarios if sc["name"] == selected_sc_name), scenarios[1])

    # 2. Master Metrics KPI Cards Grid
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        render_kpi_card("Total Capex", investment_total, tooltip="Total renovation capex under long-term loan")
    with c2:
        render_kpi_card("Annual Debt Service", debt_service, tooltip="Fixed annual debt repayment over 30 yrs")
    with c3:
        render_kpi_card("Incremental Rev", current_scenario["additional_annual_revenue"], highlight=True, tooltip="Estimated annual incremental revenue")
    with c4:
        render_kpi_card("Net Annual Impact", current_scenario["net_annual_impact"], tooltip="Incremental Revenue minus Debt Service")
    with c5:
        render_kpi_card("Payback Period", current_scenario["payback_years"], prefix="", suffix=" Yrs", tooltip="Estimated payback timeline")
    with c6:
        render_kpi_card("30-Year NPV", current_scenario["npv_30yr"], tooltip="30-Yr Net Present Value @ 5% discount rate")

    st.markdown("---")

    # 3. Revenue Streams Breakdown Pie Chart & Callouts
    col_left, col_right = st.columns(2)
    
    with col_left:
        bd = current_scenario.get("breakdown", {})
        df_bd = pd.DataFrame([
            {"Stream": "VIP Hospitality", "Value (€M)": bd.get("vip_hospitality", 0)},
            {"Stream": "Concerts & Events", "Value (€M)": bd.get("concerts_and_events", 0)},
            {"Stream": "Museum & Tours", "Value (€M)": bd.get("museum_and_tours", 0)},
            {"Stream": "NFL & Major Sports", "Value (€M)": bd.get("nfl_and_sports", 0)},
            {"Stream": "Retail & Catering", "Value (€M)": bd.get("retail_and_catering", 0)},
        ])
        
        fig_pie = px.pie(
            df_bd,
            names="Stream",
            values="Value (€M)",
            title=f"Incremental Revenue Streams Breakdown ({selected_sc_name})",
            hole=0.4,
            color_discrete_sequence=[COLOR_GOLD, COLOR_BLUE, COLOR_GREEN, COLOR_PURPLE, COLOR_PINK]
        )
        fig_pie.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=330)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; gap: 1rem; justify-content: center; height: 100%;">
            <div style="padding: 1rem; background: #111827; border: 1px solid #1F2937; border-left: 4px solid #F59E0B; border-radius: 8px;">
                <div style="font-weight: 700; color: #F59E0B; margin-bottom: 0.25rem;">
                    🏟️ 365-Day Venue Monetization
                </div>
                <p style="font-size: 0.85rem; color: #9CA3AF; line-height: 1.4; margin: 0;">
                    The retractable pitch system enables hosting 50+ major non-football events, mega concerts (Taylor Swift, Karol G), NFL International games, and corporate expos annually without compromising pitch quality.
                </p>
            </div>

            <div style="padding: 1rem; background: #111827; border: 1px solid #1F2937; border-left: 4px solid #3B82F6; border-radius: 8px;">
                <div style="font-weight: 700; color: #3B82F6; margin-bottom: 0.25rem;">
                    👑 Premium VIP & Hospitality Expansion
                </div>
                <p style="font-size: 0.85rem; color: #9CA3AF; line-height: 1.4; margin: 0;">
                    Hospitality capacity tripled with luxury skyboxes, 360-degree LED ring display, and fine dining, driving matchday yield per seat from €80 to €175+.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 4. Downside Risk & Stress Testing Simulator
    if stress_data and "scenarios" in stress_data:
        st.markdown("---")
        st.markdown("### ⚠️ Downside Risk & Stress Testing Simulator")
        st.caption("Simulates financial resilience under severe sporting underperformance (early UCL exit) and macroeconomic shocks (wage inflation).")
        
        df_stress = pd.DataFrame(stress_data["scenarios"])
        display_stress = df_stress[[
            "name", "ucl_prize_money", "revenue_impact", 
            "net_profit_impact", "result_profit", "status"
        ]].copy()
        display_stress.columns = [
            "Stress Test Scenario", "UCL Prize Money (€M)", "Revenue Impact (€M)", 
            "Net Profit Impact (€M)", "Resulting Net Profit (€M)", "Risk Status"
        ]
        st.dataframe(display_stress, use_container_width=True, hide_index=True)
