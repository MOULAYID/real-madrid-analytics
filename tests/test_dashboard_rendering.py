"""Regression checks for dashboard rendering and portable data fidelity."""
import csv
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest
from backend.main import app
from scripts.build_static_dashboard import build

def test_dashboard_renders_without_exceptions():
    dashboard = AppTest.from_file("dashboard/app.py").run(timeout=60)
    assert not dashboard.exception
    assert len(dashboard.tabs) == 8
    assert dashboard.selectbox[0].value == "2024/25"

def test_static_data_matches_api_for_each_season(tmp_path):
    snapshot = build(tmp_path)
    client = TestClient(app)
    for season, expected in snapshot["overviewBySeason"].items():
        assert expected == client.get("/api/overview", params={"season": season}).json()
    for endpoint, expected in snapshot["endpoints"].items():
        assert expected == client.get("/api/" + endpoint).json()
    with (tmp_path / "exports" / "financials.csv").open(encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    assert len(rows) == len(snapshot["overviewBySeason"])
    assert "revenue_total" in rows[0]
