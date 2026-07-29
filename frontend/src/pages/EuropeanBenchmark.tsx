import React from 'react';
import { 
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis, BarChart, Bar, Legend, Cell 
} from 'recharts';

interface EuropeanBenchmarkProps {
  data: any;
}

const CLUB_COLORS: Record<string, string> = {
  "Real Madrid": "#f59e0b",
  "Manchester City": "#3b82f6",
  "Paris Saint-Germain": "#8b5cf6",
  "FC Barcelona": "#ec4899",
  "Bayern Munich": "#ef4444",
  "Liverpool FC": "#10b981"
};

export const EuropeanBenchmark: React.FC<EuropeanBenchmarkProps> = ({ data }) => {
  if (!data) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading European Benchmark...</div>;

  const { clubs, positioning_matrix } = data;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Competitive Positioning Matrix (Scatter Plot) */}
      <div className="card">
        <div className="chart-title">
          <span>European Elite Competitive Positioning Matrix</span>
          <span className="badge badge-gold">Financial Power vs Sporting Success</span>
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
          Top-right quadrant represents absolute football dominance (High Financial Resilience + Elite Silverware Output).
        </div>
        <div style={{ height: '360px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis 
                type="number" 
                dataKey="financial_power" 
                name="Financial Power Index" 
                domain={[60, 100]} 
                stroke="var(--text-muted)"
                label={{ value: 'Financial Power Index (0-100)', position: 'bottom', fill: 'var(--text-muted)', fontSize: 12 }} 
              />
              <YAxis 
                type="number" 
                dataKey="sporting_success" 
                name="Sporting Success Index" 
                domain={[60, 100]} 
                stroke="var(--text-muted)"
                label={{ value: 'Sporting Success Index (0-100)', angle: -90, position: 'left', fill: 'var(--text-muted)', fontSize: 12 }} 
              />
              <ZAxis type="number" dataKey="revenue" range={[100, 600]} name="Revenue" unit="M €" />
              <Tooltip 
                cursor={{ strokeDasharray: '3 3' }}
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const c = payload[0].payload;
                    return (
                      <div style={{ backgroundColor: '#111827', border: '1px solid #374151', padding: '0.75rem', borderRadius: '0.5rem', color: '#fff' }}>
                        <div style={{ fontWeight: 'bold', color: CLUB_COLORS[c.club] || '#fff' }}>{c.club}</div>
                        <div style={{ fontSize: '0.8rem' }}>Revenue: €{c.revenue}M</div>
                        <div style={{ fontSize: '0.8rem' }}>Wage Ratio: {c.wage_ratio}%</div>
                        <div style={{ fontSize: '0.8rem' }}>Squad Value: €{c.squad_value}M</div>
                        <div style={{ fontSize: '0.8rem' }}>5-Yr Trophies: {c.trophies}</div>
                        <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--accent-gold)' }}>Financial Power Score: {c.financial_power}</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Scatter name="Clubs" data={positioning_matrix} fill="#3b82f6">
                {positioning_matrix.map((entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={CLUB_COLORS[entry.club] || '#3b82f6'} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Side-by-Side Revenue Comparison Chart */}
      <div className="card">
        <div className="chart-title">
          <span>Deloitte Money League Top Clubs Total Revenue Comparison (€ Millions)</span>
          <span className="badge badge-blue">Global Leaderboard</span>
        </div>
        <div style={{ height: '300px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={clubs}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="club" stroke="var(--text-muted)" fontSize={12} />
              <YAxis stroke="var(--text-muted)" fontSize={12} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                formatter={(val: any) => [`€${val}M`]}
              />
              <Legend wrapperStyle={{ paddingTop: '10px' }} />
              <Bar dataKey="commercial_revenue" name="Commercial (€M)" stackId="a" fill="#f59e0b" />
              <Bar dataKey="broadcasting_revenue" name="Broadcasting (€M)" stackId="a" fill="#3b82f6" />
              <Bar dataKey="matchday_revenue" name="Matchday (€M)" stackId="a" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Multi-Club Comprehensive Data Table */}
      <div className="card">
        <div className="chart-title">
          <span>Elite European Peer Group Financial & Sporting Benchmark Table</span>
        </div>
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Club Name</th>
                <th>Revenue (€M)</th>
                <th>Commercial (€M)</th>
                <th>Wage Ratio (%)</th>
                <th>Net Debt (€M)</th>
                <th>Squad Value (€M)</th>
                <th>5-Yr Net Spend (€M)</th>
                <th>5-Yr Trophies</th>
              </tr>
            </thead>
            <tbody>
              {clubs.map((c: any, idx: number) => (
                <tr key={idx} style={{ background: c.club === 'Real Madrid' ? 'rgba(245,158,11,0.1)' : 'transparent' }}>
                  <td style={{ fontWeight: 700, color: c.club === 'Real Madrid' ? 'var(--accent-gold)' : 'var(--text-main)' }}>
                    {c.club} {c.club === 'Real Madrid' ? '👑' : ''}
                  </td>
                  <td style={{ fontWeight: 600 }}>€{c.revenue}M</td>
                  <td>€{c.commercial_revenue}M</td>
                  <td style={{ color: c.wage_ratio > 65 ? 'var(--accent-red)' : 'var(--accent-green)', fontWeight: 600 }}>
                    {c.wage_ratio}%
                  </td>
                  <td style={{ color: c.net_debt < 0 ? 'var(--accent-green)' : 'var(--text-main)' }}>
                    {c.net_debt < 0 ? `Net Cash (€${Math.abs(c.net_debt)}M)` : `€${c.net_debt}M`}
                  </td>
                  <td>€{c.squad_value}M</td>
                  <td>€{c.five_yr_net_transfer_spend}M</td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>{c.five_yr_trophies}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
