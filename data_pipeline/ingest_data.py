"""
Enriched Data Ingestion & Star Schema Populator with Advanced Financial Dimensions
(Commercial Sub-segments, Capital Gains, Cash Flow Decomposition, Stress Testing, ESG & Femenino)
"""
import os
import json
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Dim_Date
seasons_data = [
    {"season": "2014/15", "year": 2015, "is_forecast": False},
    {"season": "2015/16", "year": 2016, "is_forecast": False},
    {"season": "2016/17", "year": 2017, "is_forecast": False},
    {"season": "2017/18", "year": 2018, "is_forecast": False},
    {"season": "2018/19", "year": 2019, "is_forecast": False},
    {"season": "2019/20", "year": 2020, "is_forecast": False},
    {"season": "2020/21", "year": 2021, "is_forecast": False},
    {"season": "2021/22", "year": 2022, "is_forecast": False},
    {"season": "2022/23", "year": 2023, "is_forecast": False},
    {"season": "2023/24", "year": 2024, "is_forecast": False},
    {"season": "2024/25", "year": 2025, "is_forecast": False},
    {"season": "2025/26", "year": 2026, "is_forecast": True},
    {"season": "2026/27", "year": 2027, "is_forecast": True},
    {"season": "2027/28", "year": 2028, "is_forecast": True},
]

# 2. Fact_Financials
financials_data = [
    {
        "season": "2014/15", "revenue_total": 577.0, "commercial_revenue": 247.3, "broadcasting_revenue": 194.9, "matchday_revenue": 134.8,
        "operating_costs": 442.0, "wages": 289.0, "player_amortization": 78.5, "ebitda": 135.0, "net_profit": 42.0,
        "cash": 109.0, "debt": 254.0, "net_debt": 145.0, "assets": 890.0, "liabilities": 540.0, "financial_health_score": 78
    },
    {
        "season": "2015/16", "revenue_total": 620.1, "commercial_revenue": 263.4, "broadcasting_revenue": 216.8, "matchday_revenue": 139.9,
        "operating_costs": 479.1, "wages": 306.4, "player_amortization": 82.0, "ebitda": 141.0, "net_profit": 30.3,
        "cash": 211.0, "debt": 224.0, "net_debt": 13.0, "assets": 930.0, "liabilities": 510.0, "financial_health_score": 84
    },
    {
        "season": "2016/17", "revenue_total": 674.6, "commercial_revenue": 301.4, "broadcasting_revenue": 236.8, "matchday_revenue": 136.4,
        "operating_costs": 527.6, "wages": 377.0, "player_amortization": 89.2, "ebitda": 147.0, "net_profit": 21.4,
        "cash": 178.0, "debt": 188.0, "net_debt": 10.0, "assets": 985.0, "liabilities": 520.0, "financial_health_score": 86
    },
    {
        "season": "2017/18", "revenue_total": 750.9, "commercial_revenue": 356.3, "broadcasting_revenue": 251.3, "matchday_revenue": 143.3,
        "operating_costs": 603.9, "wages": 395.0, "player_amortization": 104.1, "ebitda": 147.0, "net_profit": 31.2,
        "cash": 190.0, "debt": 83.0, "net_debt": -107.0, "assets": 1050.0, "liabilities": 515.0, "financial_health_score": 92
    },
    {
        "season": "2018/19", "revenue_total": 757.3, "commercial_revenue": 371.3, "broadcasting_revenue": 241.6, "matchday_revenue": 144.4,
        "operating_costs": 581.3, "wages": 394.2, "player_amortization": 108.5, "ebitda": 176.0, "net_profit": 38.4,
        "cash": 156.0, "debt": 128.0, "net_debt": -27.0, "assets": 1120.0, "liabilities": 530.0, "financial_health_score": 90
    },
    {
        "season": "2019/20", "revenue_total": 714.9, "commercial_revenue": 339.4, "broadcasting_revenue": 255.5, "matchday_revenue": 120.0,
        "operating_costs": 537.9, "wages": 411.0, "player_amortization": 122.0, "ebitda": 177.0, "net_profit": 0.3,
        "cash": 125.0, "debt": 366.0, "net_debt": 241.0, "assets": 1180.0, "liabilities": 620.0, "financial_health_score": 80
    },
    {
        "season": "2020/21", "revenue_total": 653.0, "commercial_revenue": 319.6, "broadcasting_revenue": 300.2, "matchday_revenue": 33.2,
        "operating_costs": 473.0, "wages": 402.0, "player_amortization": 115.0, "ebitda": 180.0, "net_profit": 0.9,
        "cash": 122.0, "debt": 390.0, "net_debt": 268.0, "assets": 1210.0, "liabilities": 650.0, "financial_health_score": 79
    },
    {
        "season": "2021/22", "revenue_total": 721.5, "commercial_revenue": 352.0, "broadcasting_revenue": 237.7, "matchday_revenue": 131.8,
        "operating_costs": 518.5, "wages": 405.0, "player_amortization": 105.0, "ebitda": 203.0, "net_profit": 12.9,
        "cash": 425.0, "debt": 700.0, "net_debt": 275.0, "assets": 1350.0, "liabilities": 780.0, "financial_health_score": 85
    },
    {
        "season": "2022/23", "revenue_total": 843.0, "commercial_revenue": 403.0, "broadcasting_revenue": 288.0, "matchday_revenue": 152.0,
        "operating_costs": 685.0, "wages": 452.0, "player_amortization": 118.0, "ebitda": 158.0, "net_profit": 11.8,
        "cash": 128.0, "debt": 1075.0, "net_debt": 47.0, "assets": 1520.0, "liabilities": 910.0, "financial_health_score": 89
    },
    {
        "season": "2023/24", "revenue_total": 1073.0, "commercial_revenue": 482.0, "broadcasting_revenue": 306.0, "matchday_revenue": 285.0,
        "operating_costs": 843.0, "wages": 505.0, "player_amortization": 132.0, "ebitda": 230.0, "net_profit": 15.6,
        "cash": 82.0, "debt": 1170.0, "net_debt": 8.0, "assets": 1780.0, "liabilities": 1050.0, "financial_health_score": 95
    },
    {
        "season": "2024/25", "revenue_total": 1185.0, "commercial_revenue": 542.0, "broadcasting_revenue": 318.0, "matchday_revenue": 325.0,
        "operating_costs": 920.0, "wages": 540.0, "player_amortization": 140.0, "ebitda": 265.0, "net_profit": 24.2,
        "cash": 115.0, "debt": 1150.0, "net_debt": -12.0, "assets": 1920.0, "liabilities": 1110.0, "financial_health_score": 97
    }
]

# 3. Commercial Sub-Segments Breakdown (€ Millions)
commercial_breakdown_data = [
    {
        "season": "2024/25",
        "adidas_kit_supplier": 120.0,
        "emirates_main_sponsor": 70.0,
        "hp_sleeve_sponsor": 70.0,
        "global_partners": 135.0,
        "retail_merchandise": 115.0,
        "tours_exhibition": 32.0,
        "total_commercial": 542.0
    },
    {
        "season": "2023/24",
        "adidas_kit_supplier": 115.0,
        "emirates_main_sponsor": 70.0,
        "hp_sleeve_sponsor": 50.0,
        "global_partners": 125.0,
        "retail_merchandise": 97.0,
        "tours_exhibition": 25.0,
        "total_commercial": 482.0
    },
    {
        "season": "2022/23",
        "adidas_kit_supplier": 110.0,
        "emirates_main_sponsor": 70.0,
        "hp_sleeve_sponsor": 0.0,
        "global_partners": 115.0,
        "retail_merchandise": 88.0,
        "tours_exhibition": 20.0,
        "total_commercial": 403.0
    }
]

# 4. Capital Gains on Player Sales (Plusvalias en Traspasos en €M)
capital_gains_data = [
    {"season": "2014/15", "player_sold": "Angel Di Maria", "sale_price": 75.0, "book_value": 20.0, "capital_gain": 55.0},
    {"season": "2017/18", "player_sold": "Alvaro Morata", "sale_price": 66.0, "book_value": 14.0, "capital_gain": 52.0},
    {"season": "2018/19", "player_sold": "Cristiano Ronaldo", "sale_price": 117.0, "book_value": 32.0, "capital_gain": 85.0},
    {"season": "2019/20", "player_sold": "Mateo Kovacic", "sale_price": 45.0, "book_value": 20.0, "capital_gain": 25.0},
    {"season": "2020/21", "player_sold": "Achraf Hakimi", "sale_price": 43.0, "book_value": 5.0, "capital_gain": 38.0},
    {"season": "2021/22", "player_sold": "Raphael Varane", "sale_price": 40.0, "book_value": 8.0, "capital_gain": 32.0},
    {"season": "2021/22", "player_sold": "Martin Odegaard", "sale_price": 35.0, "book_value": 7.0, "capital_gain": 28.0},
    {"season": "2022/23", "player_sold": "Casemiro", "sale_price": 70.6, "book_value": 5.6, "capital_gain": 65.0}
]

# 5. 3-Statement Cash Flow Decomposition (€ Millions)
cash_flow_data = [
    {
        "season": "2024/25",
        "operating_cash_flow": 285.0,
        "investing_cash_flow": -180.0,
        "financing_cash_flow": -72.0,
        "net_cash_change": 33.0,
        "ending_cash_balance": 115.0
    },
    {
        "season": "2023/24",
        "operating_cash_flow": 245.0,
        "investing_cash_flow": -230.0,
        "financing_cash_flow": -61.0,
        "net_cash_change": -46.0,
        "ending_cash_balance": 82.0
    },
    {
        "season": "2022/23",
        "operating_cash_flow": 182.0,
        "investing_cash_flow": -415.0,
        "financing_cash_flow": 136.0,
        "net_cash_change": -97.0,
        "ending_cash_balance": 128.0
    }
]

# 6. Downside Stress Testing & Sensitivity Analysis
stress_testing_data = {
    "base_season": "2024/25",
    "base_revenue": 1185.0,
    "base_net_profit": 24.2,
    "scenarios": [
        {
            "id": "ucl_winner",
            "name": "Base Case: UCL Winner / Finalist",
            "ucl_prize_money": 140.0,
            "revenue_impact": 0.0,
            "net_profit_impact": 0.0,
            "result_profit": 24.2,
            "status": "Target Baseline"
        },
        {
            "id": "ucl_r16_exit",
            "name": "Stress Scenario A: Early UCL Exit (Round of 16)",
            "ucl_prize_money": 65.0,
            "revenue_impact": -75.0,
            "net_profit_impact": -55.0,
            "result_profit": -30.8,
            "status": "High Risk Warning"
        },
        {
            "id": "wage_inflation_10pct",
            "name": "Stress Scenario B: 10% External Wage Inflation",
            "wage_cost_increase": 54.0,
            "revenue_impact": 0.0,
            "net_profit_impact": -54.0,
            "result_profit": -29.8,
            "status": "Medium Risk"
        },
        {
            "id": "combined_shock",
            "name": "Stress Scenario C: Combined Shock (Early Exit + Wage Shock)",
            "ucl_prize_money": 65.0,
            "revenue_impact": -75.0,
            "net_profit_impact": -109.0,
            "result_profit": -84.8,
            "status": "Severe Shock Threshold"
        }
    ]
}

# 7. Real Madrid Femenino & ESG Sustainability Metrics
esg_femenino_data = {
    "femenino_analytics": [
        {"season": "2020/21", "revenue": 1.2, "wages": 2.5, "wage_ratio": 208.3, "league_finish": 2},
        {"season": "2021/22", "revenue": 3.4, "wages": 4.1, "wage_ratio": 120.6, "league_finish": 3},
        {"season": "2022/23", "revenue": 5.8, "wages": 5.9, "wage_ratio": 101.7, "league_finish": 2},
        {"season": "2023/24", "revenue": 8.1, "wages": 7.2, "wage_ratio": 88.9, "league_finish": 2},
        {"season": "2024/25", "revenue": 10.5, "wages": 8.5, "wage_ratio": 81.0, "league_finish": 2}
    ],
    "esg_governance": {
        "stadium_environmental_certification": "LEED Gold Certified",
        "renewable_energy_share": 100.0,
        "annual_solar_generation_gwh": 3.2,
        "water_recycling_efficiency_pct": 85.0,
        "local_madrid_economic_impact_annual": 450.0,
        "direct_jobs_supported": 3400
    }
}

# Save enhanced JSON files
with open(os.path.join(DATA_DIR, "financials.json"), "w", encoding="utf-8") as f:
    json.dump(financials_data, f, indent=2)

with open(os.path.join(DATA_DIR, "commercial_breakdown.json"), "w", encoding="utf-8") as f:
    json.dump(commercial_breakdown_data, f, indent=2)

with open(os.path.join(DATA_DIR, "capital_gains.json"), "w", encoding="utf-8") as f:
    json.dump(capital_gains_data, f, indent=2)

with open(os.path.join(DATA_DIR, "cash_flow.json"), "w", encoding="utf-8") as f:
    json.dump(cash_flow_data, f, indent=2)

with open(os.path.join(DATA_DIR, "stress_testing.json"), "w", encoding="utf-8") as f:
    json.dump(stress_testing_data, f, indent=2)

with open(os.path.join(DATA_DIR, "esg_femenino.json"), "w", encoding="utf-8") as f:
    json.dump(esg_femenino_data, f, indent=2)

# Populate SQLite Database
db_path = os.path.join(DATA_DIR, "real_madrid_analytics.db")
conn = sqlite3.connect(db_path)

df_seasons = pd.DataFrame(seasons_data)
df_seasons.to_sql("dim_financial_seasons", conn, if_exists="replace", index=False)

df_fin = pd.DataFrame(financials_data)
df_fin.to_sql("fact_financials", conn, if_exists="replace", index=False)

conn.close()

print("[SUCCESS] Enhanced datasets & SQLite Star Schema populated successfully!")
