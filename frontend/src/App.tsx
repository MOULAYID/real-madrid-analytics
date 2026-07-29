import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { Navigation } from './components/Navigation';
import { ExecutiveOverview } from './pages/ExecutiveOverview';
import { RevenueEngine } from './pages/RevenueEngine';
import { CostEfficiency } from './pages/CostEfficiency';
import { SquadAnalytics } from './pages/SquadAnalytics';
import { SportingROI } from './pages/SportingROI';
import { BernabeuImpact } from './pages/BernabeuImpact';
import { EuropeanBenchmark } from './pages/EuropeanBenchmark';
import { EsgFemenino } from './pages/EsgFemenino';
import { TrendDrawer } from './components/TrendDrawer';

const API_BASE = 'http://localhost:8000/api';

// Fallback datasets for static hosting (GitHub Pages)
import financialsRaw from '../../data/financials.json';
import forecastRaw from '../../data/financials_forecast.json';
import commercialRaw from '../../data/commercial_breakdown.json';
import capitalGainsRaw from '../../data/capital_gains.json';
import cashFlowRaw from '../../data/cash_flow.json';
import stressRaw from '../../data/stress_testing.json';
import esgRaw from '../../data/esg_femenino.json';
import playerRaw from '../../data/player_economics.json';
import benchmarkRaw from '../../data/benchmark.json';
import sportingRaw from '../../data/sporting.json';
import trendsRaw from '../../data/trend_alerts.json';

export function App() {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [selectedSeason, setSelectedSeason] = useState<string>('2024/25');
  const [showForecast, setShowForecast] = useState<boolean>(true);
  const [isTrendOpen, setIsTrendOpen] = useState<boolean>(false);

  // Default initial state with fallback data for static GitHub Pages hosting
  const [overviewData, setOverviewData] = useState<any>({
    season: "2024/25",
    revenue_total: 1185.0,
    ebitda: 265.0,
    net_profit: 24.2,
    wage_ratio: 45.6,
    financial_health_score: 97,
    commercial_revenue: 542.0,
    broadcasting_revenue: 318.0,
    matchday_revenue: 325.0,
    wages: 540.0,
    net_debt: -12.0,
    cash: 115.0,
    historical_revenue: financialsRaw,
    forecast: forecastRaw.filter((r: any) => r.is_forecast)
  });
  
  const [revenueData, setRevenueData] = useState<any>({
    historical: financialsRaw,
    commercial_subsegments: commercialRaw,
    forecast: forecastRaw
  });

  const [costData, setCostData] = useState<any>({
    historical: financialsRaw,
    latest_waterfall: {
      season: "2024/25",
      revenue: 1185.0,
      wages: 540.0,
      player_amortization: 140.0,
      other_operating_costs: 240.0,
      ebitda: 265.0,
      net_profit: 24.2
    }
  });

  const [squadData, setSquadData] = useState<any>({
    squad: playerRaw,
    capital_gains: capitalGainsRaw
  });

  const [sportingRoiData, setSportingRoiData] = useState<any>({
    sporting_history: sportingRaw.map((s: any) => {
      const fin: any = financialsRaw.find((f: any) => f.season === s.season) || {};
      const trophy_points = (s.trophies * 25) + (s.league_position === 1 ? 30 : 15) + (s.champions_league_result === 'Winner' ? 40 : 20);
      const fin_investment = ((fin.wages || 400) + (fin.player_amortization || 100)) / 100.0;
      return {
        ...s,
        revenue_total: fin.revenue_total || 700,
        wages: fin.wages || 400,
        football_roi_score: Number((trophy_points / fin_investment).toFixed(2))
      };
    })
  });

  const [stadiumData, setStadiumData] = useState<any>({
    bernabeu_business_case: {
      total_capex: 1170.0,
      incremental_annual_revenue: 260.0,
      net_annual_cash_flow: 194.0,
      npv_30_year: 1620.0,
      payback_period_years: 9.2
    }
  });

  const [benchmarkData, setBenchmarkData] = useState<any>(benchmarkRaw);
  const [cashFlowData, setCashFlowData] = useState<any>(cashFlowRaw);
  const [stressData, setStressData] = useState<any>(stressRaw);
  const [esgData, setEsgData] = useState<any>(esgRaw);
  const [trends, setTrends] = useState<any[]>(trendsRaw);

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  useEffect(() => {
    fetch(`${API_BASE}/overview?season=${selectedSeason}`)
      .then(res => res.json())
      .then(data => setOverviewData(data))
      .catch(err => console.log("Using static data fallback for overview:", err));
  }, [selectedSeason]);

  useEffect(() => {
    fetch(`${API_BASE}/revenue`).then(res => res.json()).then(data => setRevenueData(data)).catch(() => {});
    fetch(`${API_BASE}/costs`).then(res => res.json()).then(data => setCostData(data)).catch(() => {});
    fetch(`${API_BASE}/squad`).then(res => res.json()).then(data => setSquadData(data)).catch(() => {});
    fetch(`${API_BASE}/sporting-roi`).then(res => res.json()).then(data => setSportingRoiData(data)).catch(() => {});
    fetch(`${API_BASE}/stadium`).then(res => res.json()).then(data => setStadiumData(data)).catch(() => {});
    fetch(`${API_BASE}/benchmark`).then(res => res.json()).then(data => setBenchmarkData(data)).catch(() => {});
    fetch(`${API_BASE}/cash-flow`).then(res => res.json()).then(data => setCashFlowData(data)).catch(() => {});
    fetch(`${API_BASE}/stress-testing`).then(res => res.json()).then(data => setStressData(data)).catch(() => {});
    fetch(`${API_BASE}/esg-femenino`).then(res => res.json()).then(data => setEsgData(data)).catch(() => {});
    fetch(`${API_BASE}/trends`).then(res => res.json()).then(data => setTrends(data)).catch(() => {});
  }, []);

  const handleExport = () => {
    window.open(`${API_BASE}/export/financials?format=csv`, '_blank');
  };

  return (
    <div className="app-container">
      <Header 
        theme={theme}
        toggleTheme={toggleTheme}
        selectedSeason={selectedSeason}
        setSelectedSeason={setSelectedSeason}
        showForecast={showForecast}
        setShowForecast={setShowForecast}
        onExport={handleExport}
        toggleTrends={() => setIsTrendOpen(!isTrendOpen)}
        trendCount={trends.length}
      />

      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="main-content">
        {activeTab === 'overview' && <ExecutiveOverview data={overviewData} cashFlowData={cashFlowData} showForecast={showForecast} />}
        {activeTab === 'revenue' && <RevenueEngine data={revenueData} showForecast={showForecast} />}
        {activeTab === 'costs' && <CostEfficiency data={costData} />}
        {activeTab === 'squad' && <SquadAnalytics data={squadData} />}
        {activeTab === 'sporting-roi' && <SportingROI data={sportingRoiData} />}
        {activeTab === 'stadium' && <BernabeuImpact data={stadiumData} stressData={stressData} />}
        {activeTab === 'benchmark' && <EuropeanBenchmark data={benchmarkData} />}
        {activeTab === 'esg-femenino' && <EsgFemenino data={esgData} />}
      </main>

      <TrendDrawer 
        isOpen={isTrendOpen} 
        onClose={() => setIsTrendOpen(false)} 
        trends={trends} 
      />
    </div>
  );
}

export default App;
