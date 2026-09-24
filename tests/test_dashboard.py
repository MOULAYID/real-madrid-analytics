"""
Unit Tests for Dashboard Data Client & Components.
"""
from dashboard.utils.api_client import (
    fetch_overview, fetch_revenue, fetch_costs, fetch_squad,
    fetch_sporting_roi, fetch_stadium, fetch_benchmark,
    fetch_cash_flow, fetch_stress_testing, fetch_esg, fetch_trends
)

def test_dashboard_api_client():
    """Test dashboard data client functions load non-empty data fallback."""
    overview = fetch_overview("2024/25")
    assert "kpis" in overview
    
    revenue = fetch_revenue()
    assert "revenue_evolution" in revenue
    
    costs = fetch_costs()
    assert "expense_waterfall" in costs
    
    squad = fetch_squad()
    assert "player_economics" in squad
    
    roi = fetch_sporting_roi()
    assert "roi_data" in roi
    
    stadium = fetch_stadium()
    assert "scenarios" in stadium
    
    benchmark = fetch_benchmark()
    assert "clubs" in benchmark
    
    cash_flow = fetch_cash_flow()
    assert isinstance(cash_flow, list) and len(cash_flow) > 0
    
    stress = fetch_stress_testing()
    assert "scenarios" in stress
    
    esg = fetch_esg()
    assert "esg_governance" in esg
    
    trends = fetch_trends()
    assert isinstance(trends, list) and len(trends) > 0
