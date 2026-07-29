import React from 'react';
import { KPICard } from '../components/KPICard';
import { 
  ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend 
} from 'recharts';

interface SportingROIProps {
  data: any;
}

export const SportingROI: React.FC<SportingROIProps> = ({ data }) => {
  if (!data) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading Sporting ROI...</div>;

  const { roi_data, summary } = data;

  const avgRoi = (roi_data.reduce((acc: number, curr: any) => acc + curr.football_roi_score, 0) / roi_data.length).toFixed(1);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Top Football ROI Score Summary */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
        <KPICard 
          title="Average Football ROI Score" 
          value={avgRoi} 
          prefix=""
          suffix=" pts / €100M"
          highlight={true}
          tooltip="Success Points (Trophies + UCL Progress + League Position) / Financial Investment (€100M Wage + Amortization)"
        />
        <KPICard 
          title="10-Year Major Trophies" 
          value={24} 
          prefix=""
          suffix=" Trophies"
          tooltip="Includes 5 Champions League titles, 4 La Liga titles, Copa del Rey, Club World Cups"
        />
        <div className="card" style={{ borderLeft: '4px solid var(--accent-gold)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>EXECUTIVE STRATEGIC SUMMARY</div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-main)', marginTop: '0.5rem', lineHeight: '1.4' }}>
            {summary}
          </p>
        </div>
      </div>

      {/* Revenue & Wage Bill vs Trophies Won per Season */}
      <div className="chart-grid">
        <div className="card">
          <div className="chart-title">
            <span>Revenue vs Trophies Won per Season</span>
            <span className="badge badge-gold">Financial Power & Silverware</span>
          </div>
          <div style={{ height: '320px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={roi_data}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="season" stroke="var(--text-muted)" fontSize={12} />
                <YAxis yAxisId="left" stroke="var(--text-muted)" fontSize={12} label={{ value: 'Revenue (€M)', angle: -90, position: 'insideLeft', fill: 'var(--text-muted)', fontSize: 11 }} />
                <YAxis yAxisId="right" orientation="right" stroke="var(--accent-gold)" fontSize={12} domain={[0, 6]} label={{ value: 'Trophies', angle: 90, position: 'insideRight', fill: 'var(--accent-gold)', fontSize: 11 }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Bar yAxisId="left" dataKey="revenue" name="Total Revenue (€M)" fill="#3b82f6" opacity={0.8} radius={[4, 4, 0, 0]} />
                <Line yAxisId="right" type="monotone" dataKey="trophies" name="Trophies Won" stroke="#f59e0b" strokeWidth={3} dot={{ r: 6 }} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Wage Bill vs Champions League Result & Football ROI Score */}
        <div className="card">
          <div className="chart-title">
            <span>Wages vs Football ROI Score Efficiency</span>
            <span className="badge badge-blue">Return on Investment</span>
          </div>
          <div style={{ height: '320px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={roi_data}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="season" stroke="var(--text-muted)" fontSize={12} />
                <YAxis yAxisId="left" stroke="var(--text-muted)" fontSize={12} />
                <YAxis yAxisId="right" orientation="right" stroke="var(--accent-green)" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Bar yAxisId="left" dataKey="wages" name="Wage Bill (€M)" fill="#8b5cf6" opacity={0.8} radius={[4, 4, 0, 0]} />
                <Line yAxisId="right" type="monotone" dataKey="football_roi_score" name="Football ROI Score" stroke="#10b981" strokeWidth={3} dot={{ r: 6 }} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Historical Season Performance Matrix */}
      <div className="card">
        <div className="chart-title">
          <span>Historical Season Sporting & Financial Performance Matrix</span>
        </div>
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Season</th>
                <th>Revenue (€M)</th>
                <th>Wage Bill (€M)</th>
                <th>La Liga Finish</th>
                <th>Champions League Stage</th>
                <th>Trophies</th>
                <th>Football ROI Score</th>
              </tr>
            </thead>
            <tbody>
              {roi_data.map((row: any, idx: number) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 600 }}>{row.season}</td>
                  <td>€{row.revenue}M</td>
                  <td>€{row.wages}M</td>
                  <td>Pos #{row.league_position}</td>
                  <td style={{ color: row.champions_league_result === 'Winner' ? 'var(--accent-gold)' : 'var(--text-main)', fontWeight: row.champions_league_result === 'Winner' ? 700 : 400 }}>
                    {row.champions_league_result}
                  </td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>{row.trophies}</td>
                  <td>
                    <span className="badge badge-gold">{row.football_roi_score}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
