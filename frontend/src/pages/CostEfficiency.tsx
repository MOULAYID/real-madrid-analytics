import React from 'react';
import { KPICard } from '../components/KPICard';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, ReferenceLine, Legend, Cell 
} from 'recharts';
import { CheckCircle } from 'lucide-react';

interface CostEfficiencyProps {
  data: any;
}

export const CostEfficiency: React.FC<CostEfficiencyProps> = ({ data }) => {
  if (!data) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading Cost Efficiency...</div>;

  const { expense_waterfall, wage_ratio_trend, transfer_efficiency } = data;
  const latestWageRatio = wage_ratio_trend[wage_ratio_trend.length - 1].wage_ratio;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Top Cost KPIs & FFP Health */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)' }}>
        <KPICard 
          title="Wage-to-Revenue Ratio" 
          value={latestWageRatio} 
          prefix=""
          suffix="%"
          highlight={true}
          tooltip="UEFA FFP recommended threshold: < 70%. Real Madrid runs at ~45.5%."
        />
        <KPICard 
          title="Net Spend Per Trophy (10 Yrs)" 
          value={transfer_efficiency.avg_net_spend_per_trophy} 
          tooltip="Total net transfer expenditure divided by major trophies won over 10 seasons"
        />
        <KPICard 
          title="Sporting Points / Net Spend" 
          value={transfer_efficiency.sporting_points_per_net_transfer} 
          prefix=""
          suffix=" pts/€M"
          tooltip="Points accumulated per €1M of net transfer spending"
        />
        <div className="card" style={{ borderLeft: latestWageRatio <= 55 ? '4px solid var(--accent-green)' : '4px solid var(--accent-gold)' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>UEFA FFP STATUS</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.5rem', fontWeight: 700, fontSize: '1.1rem', color: 'var(--accent-green)' }}>
            <CheckCircle className="w-5 h-5 text-emerald-500" />
            <span>Exemplary Compliance</span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
            24.5% below UEFA's 70% threshold limit
          </p>
        </div>
      </div>

      {/* Expense Waterfall for Latest Season */}
      <div className="chart-grid">
        <div className="card">
          <div className="chart-title">
            <span>2024/25 Financial Expense Waterfall (€ Millions)</span>
            <span className="badge badge-gold">P&L Flow</span>
          </div>
          <div style={{ height: '320px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={expense_waterfall}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={11} interval={0} angle={-15} textAnchor="end" />
                <YAxis stroke="var(--text-muted)" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                  formatter={(value: any) => [`€${Math.abs(Number(value))}M`]}
                />
                <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]}>
                  {expense_waterfall.map((entry: any, idx: number) => (
                    <Cell key={`cell-${idx}`} fill={entry.is_total ? '#10b981' : entry.value < 0 ? '#ef4444' : '#3b82f6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Wage Ratio Trend vs UEFA FFP Threshold */}
        <div className="card">
          <div className="chart-title">
            <span>Wage-to-Revenue Ratio vs UEFA FFP Cap (%)</span>
            <span className="badge badge-blue">Financial Sustainability</span>
          </div>
          <div style={{ height: '320px', width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={wage_ratio_trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="season" stroke="var(--text-muted)" fontSize={12} />
                <YAxis stroke="var(--text-muted)" fontSize={12} domain={[30, 80]} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#f3f4f6' }}
                  formatter={(value: any) => [`${value}%`]}
                />
                <Legend wrapperStyle={{ paddingTop: '10px' }} />
                <ReferenceLine y={70} label={{ value: 'UEFA FFP Limit (70%)', fill: '#ef4444', fontSize: 12 }} stroke="#ef4444" strokeDasharray="5 5" strokeWidth={2} />
                <ReferenceLine y={55} label={{ value: 'Optimal Target (55%)', fill: '#10b981', fontSize: 12 }} stroke="#10b981" strokeDasharray="3 3" />
                <Line type="monotone" dataKey="wage_ratio" name="Real Madrid Wage Ratio (%)" stroke="#f59e0b" strokeWidth={3} dot={{ r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
