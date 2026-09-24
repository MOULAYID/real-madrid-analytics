"""
Unit Tests for Data Pipeline and ML Forecasting.
"""
import os
import json
import sqlite3
import runpy

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
PIPELINE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data_pipeline")

def test_data_ingestion():
    """Test ETL ingestion creates SQLite DB and exported JSON files."""
    runpy.run_path(os.path.join(PIPELINE_DIR, "ingest_data.py"))
    
    db_path = os.path.join(DATA_DIR, "real_madrid_analytics.db")
    assert os.path.exists(db_path), "Database file real_madrid_analytics.db missing"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM dim_financial_seasons")
    count = cursor.fetchone()[0]
    conn.close()
    
    assert count >= 10, f"Expected at least 10 seasons in DB, found {count}"
    
    required_jsons = [
        "financials.json", "transfers.json", "sporting.json", 
        "player_economics.json", "benchmark.json", "commercial_breakdown.json"
    ]
    for filename in required_jsons:
        path = os.path.join(DATA_DIR, filename)
        assert os.path.exists(path), f"JSON file {filename} missing"
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert len(data) > 0, f"JSON file {filename} is empty"

def test_ml_forecasting():
    """Test ML Ridge regression forecasting model generates predictions."""
    runpy.run_path(os.path.join(PIPELINE_DIR, "forecasting.py"))
    
    forecast_path = os.path.join(DATA_DIR, "forecast_only.json")
    full_path = os.path.join(DATA_DIR, "financials_forecast.json")
    
    assert os.path.exists(forecast_path), "forecast_only.json missing"
    assert os.path.exists(full_path), "financials_forecast.json missing"
    
    with open(forecast_path, "r", encoding="utf-8") as f:
        forecast_data = json.load(f)
        assert len(forecast_data) == 3, f"Expected 3 forecast seasons, got {len(forecast_data)}"
        for item in forecast_data:
            assert item.get("is_forecast") is True
            assert item.get("revenue_total") > 1000.0, "Forecasted revenue should exceed €1,000M"
