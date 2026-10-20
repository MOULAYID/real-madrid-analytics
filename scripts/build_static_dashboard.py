"""Export the existing analytics routes as a portable GitHub Pages data snapshot."""
from pathlib import Path
import json
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.routes import analytics  # noqa: E402

def build(output_dir: Path = ROOT / "docs" / "data") -> dict:
    financials = analytics.load_json("financials_forecast.json")
    endpoints = {
        "overview": analytics.get_overview("2024/25"),
        "revenue": analytics.get_revenue_engine(),
        "costs": analytics.get_cost_structure(),
        "squad": analytics.get_squad_analytics(),
        "sporting-roi": analytics.get_sporting_roi(),
        "stadium": analytics.get_stadium_impact(),
        "benchmark": analytics.get_european_benchmark(),
        "cash-flow": analytics.get_cash_flow(),
        "stress-testing": analytics.get_stress_testing(),
        "esg-femenino": analytics.get_esg_femenino(),
        "forecast": analytics.get_forecast(),
        "trends": analytics.get_trend_alerts(),
    }
    snapshot = {
        "schemaVersion": 1,
        "overviewBySeason": {row["season"]: analytics.get_overview(row["season"]) for row in financials},
        "endpoints": endpoints,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "analytics.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    exports = output_dir / "exports"
    exports.mkdir(exist_ok=True)
    pd.DataFrame(financials).to_csv(exports / "financials.csv", index=False)
    print(f"Exported {len(endpoints)} endpoints and {len(snapshot['overviewBySeason'])} seasons to {output_dir}")
    return snapshot

if __name__ == "__main__":
    build()
