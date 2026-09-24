"""
Real Madrid Analytics Styling System
Provides custom CSS injection and Plotly dark theme configuration.
"""
import streamlit as st

def apply_custom_styles():
    """Injects custom CSS into the Streamlit app for executive dark theme."""
    custom_css = """
    <style>
    /* Global Base Settings */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    /* Header Container */
    .rm-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: linear-gradient(135deg, #111827 0%, #1F2937 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    .rm-title-group {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .rm-title {
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        background: linear-gradient(90deg, #FFFFFF 0%, #E5E7EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .rm-subtitle {
        font-size: 0.85rem;
        color: #9CA3AF;
        margin-top: 0.2rem;
    }
    
    /* Metric / KPI Card Styling */
    .kpi-card {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .kpi-card:hover {
        border-color: #4B5563;
        transform: translateY(-2px);
    }
    
    .kpi-card-highlight {
        background: linear-gradient(135deg, #1E1B4B 0%, #1E293B 100%);
        border: 1px solid #6366F1;
        border-left: 4px solid #F59E0B;
    }
    
    .kpi-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9CA3AF;
        margin-bottom: 0.35rem;
    }
    
    .kpi-value-container {
        display: flex;
        align-items: baseline;
        gap: 0.5rem;
    }
    
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #F9FAFB;
    }
    
    .kpi-change-positive {
        font-size: 0.8rem;
        font-weight: 700;
        color: #10B981;
    }
    
    .kpi-change-negative {
        font-size: 0.8rem;
        font-weight: 700;
        color: #EF4444;
    }
    
    .kpi-tooltip {
        font-size: 0.72rem;
        color: #6B7280;
        margin-top: 0.35rem;
        line-height: 1.3;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.72rem;
        font-weight: 700;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-gold {
        background-color: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .badge-blue {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .badge-green {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .badge-red {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Insights Banner */
    .insights-banner {
        background: linear-gradient(90deg, rgba(30,58,138,0.3) 0%, rgba(245,158,11,0.15) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }

    /* Table Styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Hide standard Streamlit header clutter */
    header[data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #111827;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1F2937;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        color: #9CA3AF;
        font-weight: 600;
        font-size: 0.88rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1F2937 !important;
        color: #F59E0B !important;
        border: 1px solid #374151;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Color Palette Constants for Plotly
COLOR_GOLD = "#F59E0B"
COLOR_BLUE = "#3B82F6"
COLOR_GREEN = "#10B981"
COLOR_RED = "#EF4444"
COLOR_PURPLE = "#8B5CF6"
COLOR_PINK = "#EC4899"
COLOR_TEXT_MUTED = "#9CA3AF"

PLOTLY_LAYOUT_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#F3F4F6", size=12),
    xaxis=dict(
        gridcolor="#1F2937",
        zerolinecolor="#374151",
        tickfont=dict(color="#9CA3AF")
    ),
    yaxis=dict(
        gridcolor="#1F2937",
        zerolinecolor="#374151",
        tickfont=dict(color="#9CA3AF")
    ),
    legend=dict(
        bgcolor="rgba(17, 24, 39, 0.8)",
        bordercolor="#374151",
        borderwidth=1,
        font=dict(color="#D1D5DB")
    ),
    margin=dict(l=40, r=40, t=40, b=40)
)
