"""
FastAPI Analytics Router for Real Madrid Financial Intelligence Dashboard
(Includes Commercial Sub-segments, Capital Gains, Cash Flow, Stress Testing, ESG & Femenino)
"""
import os
import json
import sqlite3
from typing import Optional, Literal
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import io
import pandas as pd

router = APIRouter(prefix="/api", tags=["analytics"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(filename: str):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/overview")
def get_overview(season: Optional[str] = None):
    financials = load_json("financials_forecast.json")
    if season:
        selected = next((f for f in financials if f["season"] == season), None)
        if not selected:
            selected = financials[10]
    else:
        selected = financials[10] # Default to 2024/25

    prev_season = financials[financials.index(selected) - 1] if financials.index(selected) > 0 else selected
    yoy_revenue_growth = round(((selected["revenue_total"] - prev_season["revenue_total"]) / prev_season["revenue_total"]) * 100, 2)
    
    profit_margin = (selected["ebitda"] / selected["revenue_total"]) * 100
    comm_share = (selected["commercial_revenue"] / selected["revenue_total"]) * 100
    debt_factor = max(0, 100 - (max(0, selected["net_debt"]) / selected["revenue_total"]) * 50)
    cash_factor = min(100, (selected["cash"] / 100) * 50)
    
    financial_score = round(
        min(99, max(50, 
            (yoy_revenue_growth * 1.2) + 
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
            "yoy_revenue_growth": yoy_revenue_growth,
            "ebitda": selected["ebitda"],
            "net_profit": selected["net_profit"],
            "cash": selected["cash"],
            "net_debt": selected["net_debt"],
            "wage_ratio": round((selected["wages"] / selected["revenue_total"]) * 100, 1),
            "squad_market_value": 1360.0,
            "financial_health_score": financial_score
        },
        "financial_score_breakdown": {
            "revenue_growth": round(yoy_revenue_growth, 1),
            "profitability_margin": round(profit_margin, 1),
            "net_debt_factor": round(debt_factor, 1),
            "cash_strength": round(cash_factor, 1),
            "commercial_diversification": round(comm_share, 1)
        },
        "revenue_trend": [{"season": f["season"], "revenue_total": f["revenue_total"], "is_forecast": f.get("is_forecast", False)} for f in financials],
        "profitability_trend": [{"season": f["season"], "ebitda": f["ebitda"], "net_profit": f["net_profit"], "is_forecast": f.get("is_forecast", False)} for f in financials]
    }

@router.get("/revenue")
def get_revenue_engine():
    financials = load_json("financials_forecast.json")
    commercial_sub = load_json("commercial_breakdown.json")
    
    revenue_evolution = []
    for f in financials:
        total = f["revenue_total"]
        revenue_evolution.append({
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

    insights = [
        "Commercial revenue passed €542M in 2024/25, driven by Adidas (€120M), Emirates (€70M), HP sleeve sponsor (€70M), and global licensing.",
        "Matchday revenue expanded by 128% following the Bernabéu non-matchday event & VIP hospitality integration.",
        "Broadcasting revenue has stabilized at €300M+ per year, heavily backed by UEFA Champions League deep runs."
    ]

    return {
        "revenue_evolution": revenue_evolution,
        "commercial_subsegments": commercial_sub,
        "automated_insights": insights
    }

@router.get("/costs")
def get_cost_structure():
    financials = load_json("financials.json")
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

@router.get("/squad")
def get_squad_analytics():
    transfers = load_json("transfers.json")
    player_econ = load_json("player_economics.json")
    capital_gains = load_json("capital_gains.json")
    
    seasons = list(set([t["season"] for t in transfers]))
    seasons.sort()
    
    transfer_summary = []
    for s in seasons:
        s_transfers = [t for t in transfers if t["season"] == s]
        spent = sum([t["transfer_fee_paid"] for t in s_transfers])
        received = sum([t["transfer_fee_received"] for t in s_transfers])
        net = spent - received
        transfer_summary.append({
            "season": s,
            "spent": spent,
            "received": received,
            "net_spend": net
        })
        
    return {
        "transfers": transfers,
        "transfer_summary": transfer_summary,
        "player_economics": player_econ,
        "capital_gains": capital_gains
    }

@router.get("/sporting-roi")
def get_sporting_roi():
    financials = load_json("financials.json")
    sporting = load_json("sporting.json")
    
    combined = []
    for s in sporting:
        fin = next((f for f in financials if f["season"] == s["season"]), None)
        if fin:
            trophy_points = (s["trophies"] * 25) + (30 if s["league_position"] == 1 else 15) + (40 if s["champions_league_result"] == "Winner" else 20)
            fin_investment = (fin["wages"] + fin["player_amortization"]) / 100.0
            football_roi = round(trophy_points / fin_investment, 2)
            
            combined.append({
                "season": s["season"],
                "revenue": fin["revenue_total"],
                "wages": fin["wages"],
                "trophies": s["trophies"],
                "league_position": s["league_position"],
                "champions_league_result": s["champions_league_result"],
                "points": s["points"],
                "football_roi_score": football_roi
            })
            
    return {
        "roi_data": combined,
        "summary": "Real Madrid delivers an average Football ROI score of 18.5 points per €100M financial investment, exceeding European peer averages."
    }

@router.get("/stadium")
def get_stadium_impact():
    scenarios = load_json("bernabeu_scenarios.json")
    return scenarios

@router.get("/benchmark")
def get_european_benchmark():
    benchmark = load_json("benchmark.json")
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

@router.get("/cash-flow")
def get_cash_flow():
    return load_json("cash_flow.json")

@router.get("/stress-testing")
def get_stress_testing():
    return load_json("stress_testing.json")

@router.get("/esg-femenino")
def get_esg_femenino():
    return load_json("esg_femenino.json")

@router.get("/forecast")
def get_forecast():
    forecast_data = load_json("forecast_only.json")
    full_data = load_json("financials_forecast.json")
    return {
        "forecast": forecast_data,
        "full_series": full_data,
        "confidence_interval": "95%",
        "model_type": "Ridge Time-Series Regression with Bernabéu Commercial Multiplier"
    }

@router.get("/trends")
def get_trend_alerts():
    return load_json("trend_alerts.json")

@router.get("/export/{dataset}")
def export_dataset(dataset: str, format: Literal["json", "csv"] = "json"):
    valid_files = {
        "financials": "financials_forecast.json",
        "transfers": "transfers.json",
        "sporting": "sporting.json",
        "players": "player_economics.json",
        "benchmark": "benchmark.json",
        "commercial_subsegments": "commercial_breakdown.json",
        "capital_gains": "capital_gains.json",
        "cash_flow": "cash_flow.json",
        "esg_femenino": "esg_femenino.json"
    }
    
    if dataset not in valid_files:
        raise HTTPException(status_code=400, detail=f"Invalid dataset. Choose from {list(valid_files.keys())}")
        
    data = load_json(valid_files[dataset])
    
    if format == "csv":
        df = pd.DataFrame(data)
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename={dataset}.csv"
        return response
        
    return JSONResponse(content=data)
