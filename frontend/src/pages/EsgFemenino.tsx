import React from 'react';
import { KPICard } from '../components/KPICard';
import { Heart } from 'lucide-react';

interface EsgFemeninoProps {
  data: any;
}

export const EsgFemenino: React.FC<EsgFemeninoProps> = ({ data }) => {
  if (!data) return <div style={{ padding: '2rem', textAlign: 'center' }}>Loading ESG & Femenino Analytics...</div>;

  const { femenino_analytics, esg_governance } = data;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* ESG Governance Highlights */}
      <div className="kpi-grid">
        <KPICard 
          title="ESG Stadium Rating" 
          value={esg_governance.stadium_environmental_certification} 
          prefix=""
          suffix=""
          highlight={true}
          tooltip="Santiago Bernabéu environmental sustainability rating"
        />
        <KPICard 
          title="Renewable Electricity Share" 
          value={esg_governance.renewable_energy_share} 
          prefix=""
          suffix="%"
          tooltip="100% green electricity powering stadium and Valdebebas training complex"
        />
        <KPICard 
          title="Annual Solar Generation" 
          value={esg_governance.annual_solar_generation_gwh} 
          prefix=""
          suffix=" GWh"
          tooltip="On-site rooftop solar panel energy generation"
        />
        <KPICard 
          title="Water Recycling Efficiency" 
          value={esg_governance.water_recycling_efficiency_pct} 
          prefix=""
          suffix="%"
          tooltip="Closed-loop rainwater harvesting and pitch irrigation system"
        />
        <KPICard 
          title="Local Economic Impact" 
          value={esg_governance.local_madrid_economic_impact_annual} 
          tooltip="Estimated annual economic contribution to Madrid regional GDP"
        />
        <KPICard 
          title="Direct Jobs Supported" 
          value={esg_governance.direct_jobs_supported} 
          prefix=""
          suffix=" Jobs"
          tooltip="Full-time staff and event venue employment"
        />
      </div>

      {/* Real Madrid Femenino Financial Evolution */}
      <div className="card">
        <div className="chart-title">
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Heart className="w-5 h-5 text-pink-500" />
            Real Madrid Femenino Commercial & Financial Evolution
          </span>
          <span className="badge badge-gold">Women's Football Growth</span>
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
          Tracking commercial revenue expansion and financial self-sustainability since official integration in 2020.
        </div>
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Season</th>
                <th>Revenue (€M)</th>
                <th>Wage Bill (€M)</th>
                <th>Wage-to-Revenue Ratio (%)</th>
                <th>Liga F Position</th>
              </tr>
            </thead>
            <tbody>
              {femenino_analytics.map((fem: any, idx: number) => (
                <tr key={idx}>
                  <td style={{ fontWeight: 600 }}>{fem.season}</td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-green)' }}>€{fem.revenue}M</td>
                  <td>€{fem.wages}M</td>
                  <td style={{ color: fem.wage_ratio <= 100 ? 'var(--accent-green)' : 'var(--accent-gold)', fontWeight: 600 }}>
                    {fem.wage_ratio}%
                  </td>
                  <td style={{ fontWeight: 700, color: 'var(--accent-gold)' }}>Runner-up (Pos #{fem.league_finish})</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
