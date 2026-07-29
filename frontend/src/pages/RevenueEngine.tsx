import React from 'react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend 
} from 'recharts';
import { Sparkles, DollarSign, Tv, Ticket, Layers } from 'lucide-react';

interface RevenueEngineProps {
  data: any;
  showForecast: boolean;
}

export const RevenueEngine: React.FC<RevenueEngineProps> = ({ data, showForecast }) => {
  if (!data) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading Revenue Engine...</div>;

  const { revenue_evolution, commercial_subsegments, automated_insights } = data;
  const filteredData = showForecast 
    ? revenue_evolution 
    : revenue_evolution.filter((item: any) => !item.is_forecast);

  const latest = filteredData[filteredData.length - 1];
  const latestCommercialSub = commercial_subsegments ? commercial_subsegments[0] : null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Revenue Stream Snapshot Header Cards */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
        <div className="card" style={{ borderLeft: '4px solid var(--accent-gold)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>
            <span>COMMERCIAL REVENUE</span>
            <DollarSign className="w-5 h-5 text-amber-500" />
          </div>
          <div className="kpi-value" style={{ margin: '0.5rem 0' }}>€{latest.commercial}M</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--accent-gold)', fontWeight: 600 }}>
            {latest.commercial_pct}% of total revenue
          </div>
        </div>

        <div className="card" style={{ borderLeft: '4px solid var(--accent-blue)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>
            <span>BROADCASTING REVENUE</span>
            <Tv className="w-5 h-5 text-blue-500" />
          </div>
          <div className="kpi-value" style={{ margin: '0.5rem 0' }}>€{latest.broadcasting}M</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--accent-blue)', fontWeight: 600 }}>
            {latest.broadcasting_pct}% of total revenue
          </div>
        </div>

        <div className="card" style={{ borderLeft: '4px solid var(--accent-green)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 600 }}>
            <span>MATCHDAY & STADIUM REVENUE</span>
            <Ticket className="w-5 h-5 text-emerald-500" />
          </div>
          <div className="kpi-value" style={{ margin: '0.5rem 0' }}>€{latest.matchday}M</div>
          <div style={{ fontSize: '0.75rem', color: 'var(--accent-green)', fontWeight: 600 }}>
            {latest.matchday_pct}% of total revenue (Bernabéu Boost)
          </div>
        </div>
      </div>

      {/* Automated AI Insights Banner */}
      <div className="card" style={{ background: 'linear-gradient(90deg, rgba(30,58,138,0.3), rgba(245,158,11,0.15))', border: '1px solid rgba(245,158,11,0.3)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', color: 'var(--accent-gold)', fontWeight: 700 }}>
          <Sparkles className="w-5 h-5" />
          <span>AUTOMATED REVENUE ENGINE INSIGHTS</span>
        </div>
        <ul style={{ paddingLeft: '1.25rem', fontSize: '0.875rem', color: 'var(--text-main)', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
          {automated_insights.map((insight: string, idx: number) => (
            <li key={idx}>{insight}</li>
          ))}
        </ul>
      </div>

      {/* Granular Commercial Income Sub-Breakdown Section */}
      {latestCommercialSub && (
        <div className="card">
          <div className="chart-title">
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Layers className="w-5 h-5 text-amber-500" />
              Granular Commercial Revenue Breakdown ({latestCommercialSub.season})
            </span>
            <span className="badge badge-gold">Commercial Sub-Segments</span>
          </div>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Commercial Sub-Segment</th>
                  <th>Primary Partners / Asset</th>
                  <th>Annual Value (€M)</th>
                  <th>Share of Commercial (%)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>Kit Supplier & Technical Partner</td>
                  <td>Adidas (10-Yr Contract + Royalties)</td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>€{latestCommercialSub.adidas_kit_supplier}M</td>
                  <td>{((latestCommercialSub.adidas_kit_supplier / latestCommercialSub.total_commercial) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>Main Shirt Sponsor</td>
                  <td>Fly Emirates</td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>€{latestCommercialSub.emirates_main_sponsor}M</td>
                  <td>{((latestCommercialSub.emirates_main_sponsor / latestCommercialSub.total_commercial) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>Sleeve Sponsor</td>
                  <td>HP (Hewlett-Packard)</td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>€{latestCommercialSub.hp_sleeve_sponsor}M</td>
                  <td>{((latestCommercialSub.hp_sleeve_sponsor / latestCommercialSub.total_commercial) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>Global & Regional Partnerships</td>
                  <td>BMW, Nivea, EA Sports, Mahou, Dubai Tourism</td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>€{latestCommercialSub.global_partners}M</td>
                  <td>{((latestCommercialSub.global_partners / latestCommercialSub.total_commercial) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>Retail, E-Commerce & Licensing</td>
                  <td>Global Stores Network & Official E-Shop</td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>€{latestCommercialSub.retail_merchandise}M</td>
                  <td>{((latestCommercialSub.retail_merchandise / latestCommercialSub.total_commercial) * 100).toFixed(1)}%</td>
                </tr>
                <tr>
                  <td style={{ fontWeight: 600, color: 'var(--text-main)' }}>International Tours & Match Fees</td>
                  :<td>US Summer Tour & FIFA Club World Cup</td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>€{latestCommercialSub.tours_exhibition}M</td>
                  <td>{((latestCommercialSub.tours_exhibition / latestCommercialSub.total_commercial) * 100).toFixed(1)}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Stacked Revenue Area Chart */}
      <div className="chart-grid">
        <div className="card">
          <div className="chart-title">
            <span>Revenue Stream Breakdown (€ Millions)</span>
            <span className="badge badge-gold">Stacked Breakdown</span>
          </div>
          <div style={{ height: '320px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={filteredData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="season" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                  formatter={(value: any) => [`€${value}M`]}
                />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Area type="monotone" dataKey="commercial" name="Commercial (€M)" stackId="1" stroke="#f59e0b" fill="#f59e0b" />
                <Area type="monotone" dataKey="broadcasting" name="Broadcasting (€M)" stackId="1" stroke="#3b82f6" fill="#3b82f6" />
                <Area type="monotone" dataKey="matchday" name="Matchday (€M)" stackId="1" stroke="#10b981" fill="#10b981" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Revenue Mix % Stacked Bar */}
        <div className="card">
          <div className="chart-title">
            <span>Revenue Mix Distribution (%)</span>
            <span className="badge badge-blue">Relative Share</span>
          </div>
          <div style={{ height: '320px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={filteredData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="season" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} domain={[0, 100]} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                  formatter={(value: any) => [`${value}%`]}
                />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <Bar dataKey="commercial_pct" name="Commercial %" stackId="a" fill="#f59e0b" />
                <Bar dataKey="broadcasting_pct" name="Broadcasting %" stackId="a" fill="#3b82f6" />
                <Bar dataKey="matchday_pct" name="Matchday %" stackId="a" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
