"""
Unit Tests for FastAPI Backend REST Endpoints.
"""
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_overview_endpoint():
    response = client.get("/api/overview?season=2024/25")
    assert response.status_code == 200
    data = response.json()
    assert "kpis" in data
    assert data["kpis"]["revenue_total"] > 1000.0

def test_revenue_endpoint():
    response = client.get("/api/revenue")
    assert response.status_code == 200
    data = response.json()
    assert "revenue_evolution" in data
    assert len(data["revenue_evolution"]) >= 10

def test_costs_endpoint():
    response = client.get("/api/costs")
    assert response.status_code == 200
    data = response.json()
    assert "expense_waterfall" in data

def test_squad_endpoint():
    response = client.get("/api/squad")
    assert response.status_code == 200
    data = response.json()
    assert "player_economics" in data

def test_sporting_roi_endpoint():
    response = client.get("/api/sporting-roi")
    assert response.status_code == 200
    data = response.json()
    assert "roi_data" in data

def test_stadium_endpoint():
    response = client.get("/api/stadium")
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data

def test_benchmark_endpoint():
    response = client.get("/api/benchmark")
    assert response.status_code == 200
    data = response.json()
    assert "clubs" in data

def test_export_endpoint():
    response = client.get("/api/export/financials?format=csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
