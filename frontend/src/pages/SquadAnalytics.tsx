import React, { useState } from 'react';
import { 
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis, BarChart, Bar, Legend, Cell 
} from 'recharts';
import { TrendingUp } from 'lucide-react';

interface SquadAnalyticsProps {
  data: any;
}

export const SquadAnalytics: React.FC<SquadAnalyticsProps> = ({ data }) => {
  const [searchTerm, setSearchTerm] = useState('');

  if (!data) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading Squad Analytics...</div>;

  const { transfer_summary, player_economics, capital_gains } = data;

  const filteredPlayers = player_economics.filter((p: any) => {
    return p.player.toLowerCase().includes(searchTerm.toLowerCase());
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Transfer Activity Breakdown Chart */}
      <div className="card">
        <div className="chart-title">
          <span>Transfer Expenditure, Sales & Net Spend per Season (€ Millions)</span>
          <span className="badge badge-gold">10-Season Transfer Strategy</span>
        </div>
        <div style={{ height: '300px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={transfer_summary}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="season" stroke="var(--text-muted)" fontSize={12} />
              <YAxis stroke="var(--text-muted)" fontSize={12} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                formatter={(value: any) => [`€${value}M`]}
              />
              <Legend wrapperStyle={{ paddingTop: '10px' }} />
              <Bar dataKey="spent" name="Fees Paid (€M)" fill="#ef4444" radius={[4, 4, 0, 0]} />
              <Bar dataKey="received" name="Fees Received (€M)" fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="net_spend" name="Net Spend (€M)" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Capital Gains on Player Sales (Plusvalías) Section */}
      {capital_gains && (
        <div className="card">
          <div className="chart-title">
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <TrendingUp className="w-5 h-5 text-emerald-500" />
              Capital Gains on Player Sales (Plusvalías en Traspasos)
            </span>
            <span className="badge badge-gold">P&L Accounting Profit</span>
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            In Spanish GAAP / IFRS football accounting, Net Profit on sales equals <span style={{ color: 'var(--text-main)', fontWeight: 600 }}>Sale Price minus Unamortized Book Value</span>.
          </div>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Season</th>
                  <th>Player Sold</th>
                  <th>Sale Price (€M)</th>
                  <th>Unamortized Book Value (€M)</th>
                  <th>Net Capital Gain (Plusvalía €M)</th>
                </tr>
              </thead>
              <tbody>
                {capital_gains.map((cg: any, idx: number) => (
                  <tr key={idx}>
                    <td>{cg.season}</td>
                    <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>{cg.player_sold}</td>
                    <td>€{cg.sale_price}M</td>
                    <td>€{cg.book_value}M</td>
                    <td style={{ fontWeight: 700, color: 'var(--accent-green)' }}>+€{cg.capital_gain}M</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Scatter Plot: Player Cost vs Sporting Performance */}
      <div className="card">
        <div className="chart-title">
          <span>Player Cost vs Sporting Contribution Matrix</span>
          <span className="badge badge-blue">Bubble Size = Market Value (€M)</span>
        </div>
        <div style={{ padding: '0.5rem 0', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          High performing, cost-efficient stars populate the top-left quadrant (e.g. Vinícius, Bellingham, Valverde). Underperformers/Injured stars land in the bottom-right quadrant.
        </div>
        <div style={{ height: '360px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis 
                type="number" 
                dataKey="salary_estimate" 
                name="Annual Salary" 
                unit="M €" 
                stroke="var(--text-muted)"
                label={{ value: 'Annual Salary (€M)', position: 'bottom', fill: 'var(--text-muted)', fontSize: 12 }} 
              />
              <YAxis 
                type="number" 
                dataKey="performance_score" 
                name="Performance Score" 
                domain={[5, 10]} 
                stroke="var(--text-muted)"
                label={{ value: 'Performance Score (Out of 10)', angle: -90, position: 'left', fill: 'var(--text-muted)', fontSize: 12 }} 
              />
              <ZAxis type="number" dataKey="market_value" range={[60, 600]} name="Market Value" unit="M €" />
              <Tooltip 
                cursor={{ strokeDasharray: '3 3' }}
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const p = payload[0].payload;
                    return (
                      <div style={{ backgroundColor: '#111827', border: '1px solid #374151', padding: '0.75rem', borderRadius: '0.5rem', color: '#fff' }}>
                        <div style={{ fontWeight: 'bold', color: 'var(--accent-gold)' }}>{p.player}</div>
                        <div style={{ fontSize: '0.8rem' }}>Salary: €{p.salary_estimate}M / yr</div>
                        <div style={{ fontSize: '0.8rem' }}>Market Value: €{p.market_value}M</div>
                        <div style={{ fontSize: '0.8rem' }}>Performance Score: {p.performance_score}/10</div>
                        <div style={{ fontSize: '0.8rem' }}>Goals + Assists: {p.goals + p.assists}</div>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Scatter name="Players" data={player_economics} fill="#3b82f6">
                {player_economics.map((entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={entry.performance_score >= 9.0 ? '#10b981' : entry.performance_score < 7.5 ? '#ef4444' : '#f59e0b'} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Player Economics Data Table */}
      <div className="card">
        <div className="chart-title">
          <span>Active Squad Player Economics & ROI Table</span>
          <input 
            type="text" 
            placeholder="Filter player..." 
            value={searchTerm} 
            onChange={(e) => setSearchTerm(e.target.value)}
            className="select-input" 
            style={{ width: '220px' }}
          />
        </div>
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Player Name</th>
                <th>Season</th>
                <th>Est. Salary (€M)</th>
                <th>Market Value (€M)</th>
                <th>Minutes Played</th>
                <th>Goals</th>
                <th>Assists</th>
                <th>Performance Score</th>
              </tr>
            </thead>
            <tbody>
              {filteredPlayers.map((p: any, idx: number) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>{p.player}</td>
                  <td>{p.season}</td>
                  <td>€{p.salary_estimate}M</td>
                  <td style={{ color: 'var(--accent-gold)', fontWeight: 600 }}>€{p.market_value}M</td>
                  <td>{p.minutes_played.toLocaleString()}</td>
                  <td>{p.goals}</td>
                  <td>{p.assists}</td>
                  <td>
                    <span className={`badge ${p.performance_score >= 9.0 ? 'badge-gold' : 'badge-blue'}`}>
                      {p.performance_score}/10
                    </span>
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
