import React from 'react';
import { KPICard } from '../components/KPICard';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend 
} from 'recharts';
import { ShieldCheck, DollarSign } from 'lucide-react';

interface ExecutiveOverviewProps {
  data: any;
  cashFlowData?: any;
  showForecast: boolean;
}

export const ExecutiveOverview: React.FC<ExecutiveOverviewProps> = ({ data, cashFlowData, showForecast }) => {
  if (!data) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading Overview Analytics...</div>;

  const { kpis, financial_score_breakdown, revenue_trend, profitability_trend } = data;

  const filteredRevenueTrend = showForecast 
    ? revenue_trend 
    : revenue_trend.filter((item: any) => !item.is_forecast);

  const filteredProfitabilityTrend = showForecast 
    ? profitability_trend 
    : profitability_trend.filter((item: any) => !item.is_forecast);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* KPI Cards Grid */}
      <div className="kpi-grid">
        <KPICard 
          title="Total Revenue" 
          value={kpis.revenue_total} 
          change={kpis.yoy_revenue_growth} 
          changeLabel="YoY"
          tooltip="Total Operating Income (Commercial + Broadcasting + Matchday)"
        />
        <KPICard 
          title="EBITDA" 
          value={kpis.ebitda} 
          tooltip="Earnings Before Interest, Tax, Depreciation & Amortization"
        />
        <KPICard 
          title="Net Profit" 
          value={kpis.net_profit} 
          tooltip="Post-tax Net Earnings reported in official annual accounts"
        />
        <KPICard 
          title="Cash Position" 
          value={kpis.cash} 
          tooltip="Liquid cash balance available at year-end"
        />
        <KPICard 
          title="Net Debt" 
          value={kpis.net_debt} 
          tooltip="Total Financial Debt minus Cash Position (Excludes Ring-fenced Long-term Stadium Loan)"
        />
        <KPICard 
          title="Wage / Revenue Ratio" 
          value={kpis.wage_ratio} 
          prefix=""
          suffix="%"
          tooltip="Staff & Player Salaries / Total Operating Revenue (UEFA FFP Guideline: < 70%)"
        />
        <KPICard 
          title="Squad Market Value" 
          value={kpis.squad_market_value} 
          tooltip="Combined Transfermarkt market valuation of the active squad"
        />
        <KPICard 
          title="Financial Health Index" 
          value={kpis.financial_health_score} 
          prefix=""
          suffix="/100"
          highlight={true}
          tooltip="Composite metric based on Revenue Growth, EBITDA margin, Net Debt leverage, Cash reserve, and Revenue diversification."
        />
      </div>

      {/* Financial Health Score & Revenue Trajectory */}
      <div className="chart-grid" style={{ gridTemplateColumns: '1fr 2fr' }}>
        <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <div className="chart-title">
              <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <ShieldCheck style={{ color: 'var(--accent-gold)' }} />
                Financial Strength Score
              </span>
              <span className="badge badge-gold">{kpis.financial_health_score}/100</span>
            </div>
            
            <div style={{ margin: '1.5rem 0', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  <span>Revenue Growth Strength</span>
                  <span>{financial_score_breakdown.revenue_growth}%</span>
                </div>
                <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', marginTop: '4px', overflow: 'hidden' }}>
                  <div style={{ width: `${Math.min(100, Math.max(10, financial_score_breakdown.revenue_growth * 4))}%`, background: 'var(--accent-blue)', height: '100%' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  <span>Profitability Margin (EBITDA)</span>
                  <span>{financial_score_breakdown.profitability_margin}%</span>
                </div>
                <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', marginTop: '4px', overflow: 'hidden' }}>
                  <div style={{ width: `${Math.min(100, financial_score_breakdown.profitability_margin * 3.5)}%`, background: 'var(--accent-green)', height: '100%' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  <span>Net Debt Leverage Factor</span>
                  <span>{financial_score_breakdown.net_debt_factor}/100</span>
                </div>
                <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', marginTop: '4px', overflow: 'hidden' }}>
                  <div style={{ width: `${financial_score_breakdown.net_debt_factor}%`, background: 'var(--accent-gold)', height: '100%' }} />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  <span>Commercial Diversification</span>
                  <span>{financial_score_breakdown.commercial_diversification}%</span>
                </div>
                <div style={{ height: '6px', background: 'var(--border-color)', borderRadius: '3px', marginTop: '4px', overflow: 'hidden' }}>
                  <div style={{ width: `${financial_score_breakdown.commercial_diversification * 2}%`, background: 'var(--accent-purple)', height: '100%' }} />
                </div>
              </div>
            </div>
          </div>

          <div style={{ padding: '0.75rem', background: 'var(--bg-secondary)', borderRadius: '0.5rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            <span style={{ fontWeight: 600, color: 'var(--accent-green)' }}>Executive Verdict:</span> Real Madrid demonstrates elite financial resilience with low net debt, zero cash-flow risk, and industry-leading revenue generation exceeding €1B.
          </div>
        </div>

        {/* Revenue 10-Yr Trend */}
        <div className="card">
          <div className="chart-title">
            <span>Revenue Trajectory (10+ Seasons)</span>
            <span className="badge badge-blue">€ Millions</span>
          </div>
          <div style={{ height: '280px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={filteredRevenueTrend}>
                <defs>
                  <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="season" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} domain={[400, 'dataMax + 100']} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                  formatter={(value: any) => [`€${value}M`, 'Revenue']}
                />
                <Area type="monotone" dataKey="revenue_total" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorRev)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* 3-Statement Cash Flow Decomposition */}
      {cashFlowData && (
        <div className="card">
          <div className="chart-title">
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <DollarSign className="w-5 h-5 text-emerald-500" />
              3-Statement Cash Flow Decomposition (€ Millions)
            </span>
            <span className="badge badge-gold">Cash Flow Mechanics</span>
          </div>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Season</th>
                  <th>Operating Cash Flow (€M)</th>
                  <th>Investing Cash Flow (Capex & Transfers)</th>
                  <th>Financing Cash Flow (Debt & Interest)</th>
                  <th>Net Cash Change</th>
                  <th>Ending Cash Balance</th>
                </tr>
              </thead>
              <tbody>
                {cashFlowData.map((cf: any, idx: number) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 600 }}>{cf.season}</td>
                    <td style={{ color: 'var(--accent-green)', fontWeight: 600 }}>+€{cf.operating_cash_flow}M</td>
                    <td style={{ color: 'var(--accent-red)' }}>€{cf.investing_cash_flow}M</td>
                    <td style={{ color: cf.financing_cash_flow >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                      {cf.financing_cash_flow >= 0 ? `+€${cf.financing_cash_flow}M` : `€${cf.financing_cash_flow}M`}
                    </td>
                    <td style={{ fontWeight: 700, color: cf.net_cash_change >= 0 ? 'var(--accent-green)' : 'var(--accent-red)' }}>
                      {cf.net_cash_change >= 0 ? `+€${cf.net_cash_change}M` : `€${cf.net_cash_change}M`}
                    </td>
                    <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>€{cf.ending_cash_balance}M</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Profitability Evolution */}
      <div className="card">
        <div className="chart-title">
          <span>Profitability Evolution (EBITDA vs Net Profit)</span>
          <span className="badge badge-gold">Operating Strength</span>
        </div>
        <div style={{ height: '300px', width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={filteredProfitabilityTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="season" stroke="var(--text-muted)" fontSize={12} />
              <YAxis stroke="var(--text-muted)" fontSize={12} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                formatter={(value: any) => [`€${value}M`]}
              />
              <Legend wrapperStyle={{ paddingTop: '10px' }} />
              <Bar dataKey="ebitda" name="EBITDA (€M)" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              <Bar dataKey="net_profit" name="Net Profit (€M)" fill="#10b981" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
