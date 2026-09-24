"""
ESG & Femenino Dashboard Page (Page 8)
"""
import streamlit as st
import pandas as pd
from dashboard.components.kpi_card import render_kpi_card

def render_esg_femenino(data: dict):
    """Renders Page 8: ESG Governance & Real Madrid Femenino."""
    if not data or "esg_governance" not in data:
        st.info("Loading ESG & Femenino analytics...")
        return
        
    esg = data["esg_governance"]
    femenino = data.get("femenino_analytics", [])

    # 1. ESG Governance Highlights
    st.markdown("### 🌱 ESG Governance & Sustainability Metrics")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card("ESG Stadium Rating", esg.get("stadium_environmental_certification", "LEED Gold"), prefix="", suffix="", highlight=True, tooltip="Santiago Bernabéu environmental sustainability rating")
    with c2:
        render_kpi_card("Renewable Energy Share", esg.get("renewable_energy_share", 100.0), prefix="", suffix="%", tooltip="100% green electricity powering stadium & complex")
    with c3:
        render_kpi_card("Annual Solar Generation", esg.get("annual_solar_generation_gwh", 3.2), prefix="", suffix=" GWh", tooltip="On-site rooftop solar panel energy generation")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4:
        render_kpi_card("Water Recycling Efficiency", esg.get("water_recycling_efficiency_pct", 88.0), prefix="", suffix="%", tooltip="Closed-loop rainwater harvesting and pitch irrigation system")
    with c5:
        render_kpi_card("Local Economic Impact", esg.get("local_madrid_economic_impact_annual", 450.0), tooltip="Estimated annual economic contribution to Madrid GDP")
    with c6:
        render_kpi_card("Direct Jobs Supported", esg.get("direct_jobs_supported", 2400), prefix="", suffix=" Jobs", tooltip="Full-time staff and event venue employment")

    st.markdown("---")

    # 2. Real Madrid Femenino Commercial & Financial Evolution
    st.markdown("### 💖 Real Madrid Femenino Commercial & Financial Growth")
    st.caption("Tracking commercial revenue expansion and financial self-sustainability since official integration in 2020.")
    
    if femenino:
        df_fem = pd.DataFrame(femenino)
        display_fem = df_fem[["season", "revenue", "wages", "wage_ratio", "league_finish"]].copy()
        display_fem.columns = ["Season", "Revenue (€M)", "Wage Bill (€M)", "Wage-to-Revenue Ratio (%)", "Liga F Position"]
        st.dataframe(display_fem, use_container_width=True, hide_index=True)
