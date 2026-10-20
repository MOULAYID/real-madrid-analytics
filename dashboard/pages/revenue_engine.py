"""
Revenue Engine Dashboard Page (Page 2)
"""
import streamlit as st
import plotly.express as px
import pandas as pd
from dashboard.utils.styles import PLOTLY_LAYOUT_TEMPLATE, COLOR_GOLD, COLOR_BLUE, COLOR_GREEN

def render_revenue_engine(data: dict, show_forecast: bool):
    """Renders Page 2: Revenue Engine."""
    if not data or "revenue_evolution" not in data:
        st.info("Loading Revenue Engine analytics...")
        return
        
    revenue_evolution = data["revenue_evolution"]
    commercial_sub = data.get("commercial_subsegments", [])
    insights = data.get("automated_insights", [])
    
    if not show_forecast:
        revenue_evolution = [r for r in revenue_evolution if not r.get("is_forecast")]
        
    latest = revenue_evolution[-1]
    latest_comm = commercial_sub[0] if commercial_sub else None

    # 1. Revenue Stream Snapshot Header Cards
    st.markdown("### 💰 Revenue Engine Performance")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.html(f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-left: 4px solid #F59E0B; border-radius: 10px; padding: 1rem 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; color: #9CA3AF; font-size: 0.75rem; font-weight: 600;">
                <span>COMMERCIAL REVENUE</span>
                <span style="font-size: 1.2rem;">💵</span>
            </div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #F9FAFB; margin: 0.4rem 0;">€{latest['commercial']}M</div>
            <div style="font-size: 0.75rem; color: #F59E0B; font-weight: 600;">{latest['commercial_pct']}% of total revenue</div>
        </div>
        """)

    with c2:
        st.html(f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-left: 4px solid #3B82F6; border-radius: 10px; padding: 1rem 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; color: #9CA3AF; font-size: 0.75rem; font-weight: 600;">
                <span>BROADCASTING REVENUE</span>
                <span style="font-size: 1.2rem;">📺</span>
            </div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #F9FAFB; margin: 0.4rem 0;">€{latest['broadcasting']}M</div>
            <div style="font-size: 0.75rem; color: #3B82F6; font-weight: 600;">{latest['broadcasting_pct']}% of total revenue</div>
        </div>
        """)

    with c3:
        st.html(f"""
        <div style="background: #111827; border: 1px solid #1F2937; border-left: 4px solid #10B981; border-radius: 10px; padding: 1rem 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; color: #9CA3AF; font-size: 0.75rem; font-weight: 600;">
                <span>MATCHDAY & STADIUM REVENUE</span>
                <span style="font-size: 1.2rem;">🎟️</span>
            </div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #F9FAFB; margin: 0.4rem 0;">€{latest['matchday']}M</div>
            <div style="font-size: 0.75rem; color: #10B981; font-weight: 600;">{latest['matchday_pct']}% of total revenue (Bernabéu Boost)</div>
        </div>
        """)

    # 2. Automated AI Insights Banner
    st.html("<div style='height: 10px;'></div>")
    st.html(f"""
    <div class="insights-banner">
        <div style="display: flex; align-items: center; gap: 0.5rem; color: #F59E0B; font-weight: 700; margin-bottom: 0.5rem;">
            <span>✨ AUTOMATED REVENUE ENGINE INSIGHTS</span>
        </div>
        <ul style="padding-left: 1.25rem; font-size: 0.88rem; color: #F3F4F6; margin: 0;">
            {"".join([f"<li>{ins}</li>" for ins in insights])}
        </ul>
    </div>
    """)

    # 3. Granular Commercial Revenue Sub-Breakdown Section
    if latest_comm:
        st.markdown(f"### 📋 Granular Commercial Revenue Breakdown ({latest_comm.get('season', '')})")
        comm_items = [
            {"Sub-Segment": "Kit Supplier & Technical Partner", "Primary Partners": "Adidas (10-Yr Contract + Royalties)", "Annual Value (€M)": f"€{latest_comm['adidas_kit_supplier']}M", "Share of Commercial (%)": f"{((latest_comm['adidas_kit_supplier'] / latest_comm['total_commercial'])*100):.1f}%"},
            {"Sub-Segment": "Main Shirt Sponsor", "Primary Partners": "Fly Emirates", "Annual Value (€M)": f"€{latest_comm['emirates_main_sponsor']}M", "Share of Commercial (%)": f"{((latest_comm['emirates_main_sponsor'] / latest_comm['total_commercial'])*100):.1f}%"},
            {"Sub-Segment": "Sleeve Sponsor", "Primary Partners": "HP (Hewlett-Packard)", "Annual Value (€M)": f"€{latest_comm['hp_sleeve_sponsor']}M", "Share of Commercial (%)": f"{((latest_comm['hp_sleeve_sponsor'] / latest_comm['total_commercial'])*100):.1f}%"},
            {"Sub-Segment": "Global & Regional Partnerships", "Primary Partners": "BMW, Nivea, EA Sports, Mahou, Dubai Tourism", "Annual Value (€M)": f"€{latest_comm['global_partners']}M", "Share of Commercial (%)": f"{((latest_comm['global_partners'] / latest_comm['total_commercial'])*100):.1f}%"},
            {"Sub-Segment": "Retail, E-Commerce & Licensing", "Primary Partners": "Global Stores Network & Official E-Shop", "Annual Value (€M)": f"€{latest_comm['retail_merchandise']}M", "Share of Commercial (%)": f"{((latest_comm['retail_merchandise'] / latest_comm['total_commercial'])*100):.1f}%"},
            {"Sub-Segment": "International Tours & Match Fees", "Primary Partners": "US Summer Tour & FIFA Club World Cup", "Annual Value (€M)": f"€{latest_comm['tours_exhibition']}M", "Share of Commercial (%)": f"{((latest_comm['tours_exhibition'] / latest_comm['total_commercial'])*100):.1f}%"},
        ]
        df_comm = pd.DataFrame(comm_items)
        st.dataframe(df_comm, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 4. Stacked Area Chart and Revenue Mix % Bar Chart
    c_left, c_right = st.columns(2)
    
    with c_left:
        df_rev = pd.DataFrame(revenue_evolution)
        fig_area = px.area(
            df_rev,
            x="season",
            y=["commercial", "broadcasting", "matchday"],
            title="Revenue Stream Breakdown (€ Millions)",
            color_discrete_sequence=[COLOR_GOLD, COLOR_BLUE, COLOR_GREEN],
            labels={"season": "Season", "value": "Revenue (€M)", "variable": "Stream"}
        )
        fig_area.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=340)
        st.plotly_chart(fig_area, use_container_width=True)

    with c_right:
        fig_bar = px.bar(
            df_rev,
            x="season",
            y=["commercial_pct", "broadcasting_pct", "matchday_pct"],
            title="Revenue Mix Distribution (%)",
            color_discrete_sequence=[COLOR_GOLD, COLOR_BLUE, COLOR_GREEN],
            labels={"season": "Season", "value": "Share (%)", "variable": "Stream"}
        )
        fig_bar.update_layout(**PLOTLY_LAYOUT_TEMPLATE, height=340)
        st.plotly_chart(fig_bar, use_container_width=True)
