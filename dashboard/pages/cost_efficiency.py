"""
Cost Efficiency Dashboard Page (Page 3)
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dashboard.components.kpi_card import render_kpi_card
from dashboard.utils.styles import PLOTLY_LAYOUT_TEMPLATE, COLOR_GOLD, COLOR_GREEN, COLOR_RED, COLOR_BLUE

def render_cost_efficiency(data: dict):
    """Renders Page 3: Cost Structure & Efficiency."""
    if not data or "expense_waterfall" not in data:
        st.info("Loading Cost Efficiency analytics...")
        return
        
    waterfall = data["expense_waterfall"]
    wage_ratio_trend = data.get("wage_ratio_trend", [])
    transfer_eff = data.get("transfer_efficiency", {})
    
    latest_wage_ratio = wage_ratio_trend[-1]["wage_ratio"] if wage_ratio_trend else 0

    # 1. Top Cost KPIs & FFP Compliance Card
    st.markdown("### 📉 Cost Structure & Financial Sustainability")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            "Wage-to-Revenue Ratio",
            latest_wage_ratio,
            prefix="",
            suffix="%",
            highlight=True,
            tooltip="UEFA FFP guideline threshold: < 70%. Real Madrid runs at ~45.5%."
        )
    with c2:
        render_kpi_card(
            "Net Spend Per Trophy (10 Yrs)",
            transfer_eff.get("avg_net_spend_per_trophy", 0),
            tooltip="Total net transfer expenditure divided by major trophies won over 10 seasons"
        )
    with c3:
        render_kpi_card(
            "Sporting Points / Net Spend",
            transfer_eff.get("sporting_points_per_net_transfer", 0),
            prefix="",
            suffix=" pts/€M",
            tooltip="Points accumulated per €1M of net transfer spending"
        )
    with c4:
        st.html("""
        <div style="background: #111827; border: 1px solid #1F2937; border-left: 4px solid #10B981; border-radius: 10px; padding: 1rem 1.25rem; height: 100%;">
            <div style="font-size: 0.75rem; font-weight: 600; color: #9CA3AF;">UEFA FFP STATUS</div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.4rem; font-weight: 700; font-size: 1.1rem; color: #10B981;">
                <span>✅ Exemplary Compliance</span>
            </div>
            <p style="font-size: 0.75rem; color: #9CA3AF; margin-top: 0.25rem;">
                24.5% below UEFA's 70% threshold limit
            </p>
        </div>
        """)

    st.markdown("---")

    # 2. Expense Waterfall & Wage Ratio Trend
    c_left, c_right = st.columns(2)
    
    with c_left:
        # Build Plotly Waterfall Chart
        wf_names = [item["name"] for item in waterfall]
        wf_vals = [item["value"] for item in waterfall]
        wf_measures = ["relative" if not item.get("is_total") else "total" for item in waterfall]
        
        fig_wf = go.Figure(go.Waterfall(
            name="P&L Flow",
            orientation="v",
            measure=wf_measures,
            x=wf_names,
            textposition="outside",
            text=[f"€{abs(v):.0f}M" for v in wf_vals],
            y=wf_vals,
            connector={"line": {"color": "#374151"}},
            decreasing={"marker": {"color": COLOR_RED}},
            increasing={"marker": {"color": COLOR_BLUE}},
            totals={"marker": {"color": COLOR_GREEN}}
        ))
        fig_wf.update_layout(
            title="2024/25 Financial Expense Waterfall (€ Millions)",
            **PLOTLY_LAYOUT_TEMPLATE,
            height=340
        )
        st.plotly_chart(fig_wf, use_container_width=True)

    with c_right:
        df_wage = pd.DataFrame(wage_ratio_trend)
        fig_line = px.line(
            df_wage,
            x="season",
            y="wage_ratio",
            title="Wage-to-Revenue Ratio vs UEFA FFP Cap (%)",
            labels={"season": "Season", "wage_ratio": "Wage Ratio (%)"}
        )
        fig_line.update_traces(line_color=COLOR_GOLD, line_width=3, mode="lines+markers")
        
        # Add Reference Lines for UEFA 70% cap and 55% target
        fig_line.add_hline(y=70, line_dash="dash", line_color=COLOR_RED, annotation_text="UEFA FFP Limit (70%)", annotation_position="top right")
        fig_line.add_hline(y=55, line_dash="dot", line_color=COLOR_GREEN, annotation_text="Optimal Target (55%)", annotation_position="bottom right")
        
        fig_line.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=340, yaxis_range=[30, 80])
        st.plotly_chart(fig_line, use_container_width=True)
