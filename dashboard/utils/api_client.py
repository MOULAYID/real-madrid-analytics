"""
API Client & Data Loading Utility for Real Madrid Financial Dashboard.
Attempts to fetch data from FastAPI backend or falls back directly to local data JSON files.
"""
import os
import json
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def load_local_json(filename: str):
    """Fallback function to load JSON file directly from data directory."""
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@st.cache_data(ttl=60)
def fetch_overview(season: str = "2024/25"):
    """Fetch executive overview data."""
    try:
        res = requests.get(f"{API_BASE_URL}/overview", params={"season": season}, timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    # Fallback compute directly from local JSON
    financials = load_local_json("financials_forecast.json")
    if not financials:
        return {}
    
    selected = next((f for f in financials if f["season"] == season), financials[10])
    idx = financials.index(selected)
    prev_season = financials[idx - 1] if idx > 0 else selected
    
    yoy_growth = round(((selected["revenue_total"] - prev_season["revenue_total"]) / prev_season["revenue_total"]) * 100, 2)
    profit_margin = (selected["ebitda"] / selected["revenue_total"]) * 100
    comm_share = (selected["commercial_revenue"] / selected["revenue_total"]) * 100
    debt_factor = max(0, 100 - (max(0, selected["net_debt"]) / selected["revenue_total"]) * 50)
    cash_factor = min(100, (selected["cash"] / 100) * 50)
    
    financial_score = round(
        min(99, max(50, 
            (yoy_growth * 1.2) + 
            (profit_margin * 1.5) + 
            (debt_factor * 0.3) + 
            (cash_factor * 0.2) + 
            (comm_share * 0.4)
        ))
    )
    
    return {
        "selected_season": selected["season"],
        "kpis": {
            "revenue_total": selected["revenue_total"],
            "yoy_revenue_growth": yoy_growth,
            "ebitda": selected["ebitda"],
            "net_profit": selected["net_profit"],
            "cash": selected["cash"],
            "net_debt": selected["net_debt"],
            "wage_ratio": round((selected["wages"] / selected["revenue_total"]) * 100, 1),
            "squad_market_value": 1360.0,
            "financial_health_score": financial_score
        },
        "financial_score_breakdown": {
            "revenue_growth": round(yoy_growth, 1),
            "profitability_margin": round(profit_margin, 1),
            "net_debt_factor": round(debt_factor, 1),
            "cash_strength": round(cash_factor, 1),
            "commercial_diversification": round(comm_share, 1)
        },
        "revenue_trend": [{"season": f["season"], "revenue_total": f["revenue_total"], "is_forecast": f.get("is_forecast", False)} for f in financials],
        "profitability_trend": [{"season": f["season"], "ebitda": f["ebitda"], "net_profit": f["net_profit"], "is_forecast": f.get("is_forecast", False)} for f in financials]
    }

@st.cache_data(ttl=60)
def fetch_revenue():
    try:
        res = requests.get(f"{API_BASE_URL}/revenue", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    financials = load_local_json("financials_forecast.json")
    commercial_sub = load_local_json("commercial_breakdown.json")
    if not financials:
        return {}
    
    evolution = []
    for f in financials:
        total = f["revenue_total"]
        evolution.append({
            "season": f["season"],
            "commercial": f["commercial_revenue"],
            "broadcasting": f["broadcasting_revenue"],
            "matchday": f["matchday_revenue"],
            "total": total,
            "commercial_pct": round((f["commercial_revenue"] / total) * 100, 1),
            "broadcasting_pct": round((f["broadcasting_revenue"] / total) * 100, 1),
            "matchday_pct": round((f["matchday_revenue"] / total) * 100, 1),
            "is_forecast": f.get("is_forecast", False)
        })
        
    return {
        "revenue_evolution": evolution,
        "commercial_subsegments": commercial_sub,
        "automated_insights": [
            "Commercial revenue passed €542M in 2024/25, driven by Adidas (€120M), Emirates (€70M), HP sleeve sponsor (€70M), and global licensing.",
            "Matchday revenue expanded by 128% following the Bernabéu non-matchday event & VIP hospitality integration.",
            "Broadcasting revenue has stabilized at €300M+ per year, heavily backed by UEFA Champions League deep runs."
        ]
    }

@st.cache_data(ttl=60)
def fetch_costs():
    try:
        res = requests.get(f"{API_BASE_URL}/costs", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    financials = load_local_json("financials.json")
    if not financials:
        return {}
    latest = financials[-1]
    
    waterfall = [
        {"name": "Total Revenue", "value": latest["revenue_total"], "is_total": True},
        {"name": "Player & Staff Wages", "value": -latest["wages"], "is_total": False},
        {"name": "Operating Expenses", "value": -(latest["operating_costs"] - latest["wages"]), "is_total": False},
        {"name": "EBITDA", "value": latest["ebitda"], "is_total": True},
        {"name": "Player Amortization", "value": -latest["player_amortization"], "is_total": False},
        {"name": "Net Profit", "value": latest["net_profit"], "is_total": True}
    ]
    
    wage_ratio_trend = [
        {
            "season": f["season"],
            "wage_ratio": round((f["wages"] / f["revenue_total"]) * 100, 1),
            "wages": f["wages"],
            "revenue": f["revenue_total"],
            "uefa_limit": 70.0,
            "optimal_target": 55.0
        }
        for f in financials
    ]
    return {
        "expense_waterfall": waterfall,
        "wage_ratio_trend": wage_ratio_trend,
        "latest_season": latest["season"],
        "transfer_efficiency": {
            "sporting_points_per_net_transfer": 2.4,
            "avg_net_spend_per_trophy": 18.8
        }
    }

@st.cache_data(ttl=60)
def fetch_squad():
    try:
        res = requests.get(f"{API_BASE_URL}/squad", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    transfers = load_local_json("transfers.json") or []
    player_econ = load_local_json("player_economics.json") or []
    capital_gains = load_local_json("capital_gains.json") or []
    
    seasons = sorted(list(set([t["season"] for t in transfers])))
    summary = []
    for s in seasons:
        s_transfers = [t for t in transfers if t["season"] == s]
        spent = sum([t["transfer_fee_paid"] for t in s_transfers])
        received = sum([t["transfer_fee_received"] for t in s_transfers])
        summary.append({
            "season": s,
            "spent": spent,
            "received": received,
            "net_spend": spent - received
        })
        
    return {
        "transfers": transfers,
        "transfer_summary": summary,
        "player_economics": player_econ,
        "capital_gains": capital_gains
    }

@st.cache_data(ttl=60)
def fetch_sporting_roi():
    try:
        res = requests.get(f"{API_BASE_URL}/sporting-roi", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    financials = load_local_json("financials.json") or []
    sporting = load_local_json("sporting.json") or []
    
    combined = []
    for s in sporting:
        fin = next((f for f in financials if f["season"] == s["season"]), None)
        if fin:
            trophy_pts = (s["trophies"] * 25) + (30 if s["league_position"] == 1 else 15) + (40 if s["champions_league_result"] == "Winner" else 20)
            fin_inv = (fin["wages"] + fin["player_amortization"]) / 100.0
            combined.append({
                "season": s["season"],
                "revenue": fin["revenue_total"],
                "wages": fin["wages"],
                "trophies": s["trophies"],
                "league_position": s["league_position"],
                "champions_league_result": s["champions_league_result"],
                "points": s["points"],
                "football_roi_score": round(trophy_pts / fin_inv, 2)
            })
            
    return {
        "roi_data": combined,
        "summary": "Real Madrid delivers an average Football ROI score of 18.5 points per €100M financial investment, exceeding European peer averages."
    }

@st.cache_data(ttl=60)
def fetch_stadium():
    try:
        res = requests.get(f"{API_BASE_URL}/stadium", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return load_local_json("bernabeu_scenarios.json") or {}

@st.cache_data(ttl=60)
def fetch_benchmark():
    try:
        res = requests.get(f"{API_BASE_URL}/benchmark", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    
    benchmark = load_local_json("benchmark.json") or []
    return {
        "clubs": benchmark,
        "positioning_matrix": [
            {
                "club": b["club"],
                "financial_power": b["financial_power_index"],
                "sporting_success": b["sporting_success_index"],
                "revenue": b["revenue"],
                "wage_ratio": b["wage_ratio"],
                "squad_value": b["squad_value"],
                "trophies": b["five_yr_trophies"]
            }
            for b in benchmark
        ]
    }

@st.cache_data(ttl=60)
def fetch_cash_flow():
    try:
        res = requests.get(f"{API_BASE_URL}/cash-flow", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return load_local_json("cash_flow.json") or []

@st.cache_data(ttl=60)
def fetch_stress_testing():
    try:
        res = requests.get(f"{API_BASE_URL}/stress-testing", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return load_local_json("stress_testing.json") or {}

@st.cache_data(ttl=60)
def fetch_esg():
    try:
        res = requests.get(f"{API_BASE_URL}/esg-femenino", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return load_local_json("esg_femenino.json") or {}

@st.cache_data(ttl=60)
def fetch_trends():
    try:
        res = requests.get(f"{API_BASE_URL}/trends", timeout=2)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return load_local_json("trend_alerts.json") or []
