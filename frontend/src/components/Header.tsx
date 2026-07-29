import { Sun, Moon, Download, TrendingUp } from 'lucide-react';

interface HeaderProps {
  theme: 'dark' | 'light';
  toggleTheme: () => void;
  selectedSeason: string;
  setSelectedSeason: (season: string) => void;
  showForecast: boolean;
  setShowForecast: (show: boolean) => void;
  onExport: () => void;
  toggleTrends?: () => void;
  trendCount?: number;
}

const SEASONS = [
  "2014/15", "2015/16", "2016/17", "2017/18", "2018/19", 
  "2019/20", "2020/21", "2021/22", "2022/23", "2023/24", "2024/25"
];

export const Header: React.FC<HeaderProps> = ({
  theme,
  toggleTheme,
  selectedSeason,
  setSelectedSeason,
  showForecast,
  setShowForecast,
  onExport,
}) => {
  return (
    <header className="header">
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <img 
          src="https://cdn-icons-png.flaticon.com/512/738/738671.png" 
          alt="Real Madrid Analytics" 
          style={{
            width: '42px', 
            height: '42px', 
            objectFit: 'contain',
            filter: 'drop-shadow(0 0 8px rgba(217, 119, 6, 0.5))'
          }} 
        />
        <div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.02em', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            REAL MADRID <span style={{ color: 'var(--accent-gold)' }}>FINANCIAL INTELLIGENCE</span>
          </h1>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            Executive Performance & Business Model Analytics
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Season:</label>
          <select 
            value={selectedSeason} 
            onChange={(e) => setSelectedSeason(e.target.value)}
            className="select-input"
          >
            {SEASONS.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>

        <button 
          onClick={() => setShowForecast(!showForecast)}
          className={`btn ${showForecast ? 'btn-primary' : 'btn-secondary'}`}
        >
          <TrendingUp className="w-4 h-4" />
          <span>{showForecast ? 'Hide Forecast' : '3-Yr Forecast'}</span>
        </button>

        <button onClick={onExport} className="btn btn-secondary">
          <Download className="w-4 h-4" />
          <span>Export</span>
        </button>

        <button onClick={toggleTheme} className="btn btn-secondary">
          {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4" />}
        </button>
      </div>
    </header>
  );
};

