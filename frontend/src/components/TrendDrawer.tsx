import { X, TrendingUp } from 'lucide-react';

interface TrendDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  trends: any[];
}

export const TrendDrawer: React.FC<TrendDrawerProps> = ({ isOpen, onClose, trends }) => {
  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed', top: 0, right: 0, bottom: 0, width: '380px', backgroundColor: 'var(--bg-secondary)',
      borderLeft: '1px solid var(--border-color)', boxShadow: '-10px 0 25px rgba(0,0,0,0.5)', zIndex: 100,
      padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', overflowY: 'auto'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ fontWeight: 800, fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <TrendingUp className="w-5 h-5 text-amber-500" />
          <span>Automated Trend Signals</span>
        </div>
        <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
          <X className="w-5 h-5" />
        </button>
      </div>

      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
        Real-time financial anomaly and trend detection engine alerts based on historical balance sheet and P&L analysis.
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {trends.map((t: any) => (
          <div 
            key={t.id} 
            className="card" 
            style={{ 
              padding: '1rem', 
              borderLeft: t.type === 'positive' ? '4px solid var(--accent-green)' : '4px solid var(--accent-gold)' 
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
              <span className="badge badge-gold" style={{ fontSize: '0.65rem' }}>{t.category}</span>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{t.season}</span>
            </div>
            <div style={{ fontWeight: 700, fontSize: '0.9rem', margin: '0.25rem 0', color: 'var(--text-main)' }}>
              {t.title}
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
              {t.message}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
