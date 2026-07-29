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

export function App() {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [selectedSeason, setSelectedSeason] = useState<string>('2024/25');
  const [showForecast, setShowForecast] = useState<boolean>(true);
  const [isTrendOpen, setIsTrendOpen] = useState<boolean>(false);

  // API State
  const [overviewData, setOverviewData] = useState<any>(null);
  const [revenueData, setRevenueData] = useState<any>(null);
  const [costData, setCostData] = useState<any>(null);
  const [squadData, setSquadData] = useState<any>(null);
  const [sportingRoiData, setSportingRoiData] = useState<any>(null);
  const [stadiumData, setStadiumData] = useState<any>(null);
  const [benchmarkData, setBenchmarkData] = useState<any>(null);
  const [cashFlowData, setCashFlowData] = useState<any>(null);
  const [stressData, setStressData] = useState<any>(null);
  const [esgData, setEsgData] = useState<any>(null);
  const [trends, setTrends] = useState<any[]>([]);

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  useEffect(() => {
    fetch(`${API_BASE}/overview?season=${selectedSeason}`)
      .then(res => res.json())
      .then(data => setOverviewData(data))
      .catch(err => console.error("Error fetching overview:", err));
  }, [selectedSeason]);

  useEffect(() => {
    fetch(`${API_BASE}/revenue`).then(res => res.json()).then(data => setRevenueData(data)).catch(console.error);
    fetch(`${API_BASE}/costs`).then(res => res.json()).then(data => setCostData(data)).catch(console.error);
    fetch(`${API_BASE}/squad`).then(res => res.json()).then(data => setSquadData(data)).catch(console.error);
    fetch(`${API_BASE}/sporting-roi`).then(res => res.json()).then(data => setSportingRoiData(data)).catch(console.error);
    fetch(`${API_BASE}/stadium`).then(res => res.json()).then(data => setStadiumData(data)).catch(console.error);
    fetch(`${API_BASE}/benchmark`).then(res => res.json()).then(data => setBenchmarkData(data)).catch(console.error);
    fetch(`${API_BASE}/cash-flow`).then(res => res.json()).then(data => setCashFlowData(data)).catch(console.error);
    fetch(`${API_BASE}/stress-testing`).then(res => res.json()).then(data => setStressData(data)).catch(console.error);
    fetch(`${API_BASE}/esg-femenino`).then(res => res.json()).then(data => setEsgData(data)).catch(console.error);
    fetch(`${API_BASE}/trends`).then(res => res.json()).then(data => setTrends(data)).catch(console.error);
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
