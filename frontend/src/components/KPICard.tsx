import React from 'react';
import { ArrowUpRight, ArrowDownRight, Info } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  prefix?: string;
  suffix?: string;
  tooltip?: string;
  highlight?: boolean;
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  change,
  changeLabel,
  prefix = '€',
  suffix = 'M',
  tooltip,
  highlight = false
}) => {
  const isPositive = change !== undefined && change >= 0;

  return (
    <div className={`card kpi-card ${highlight ? 'border-amber-500/50 bg-amber-500/5' : ''}`}>
      <div className="flex items-center justify-between">
        <span className="kpi-title">{title}</span>
        {tooltip && (
          <div className="group relative cursor-pointer">
            <Info className="w-4 h-4 text-gray-400 hover:text-white" />
            <div className="absolute right-0 top-6 hidden group-hover:block bg-gray-900 border border-gray-700 text-xs text-gray-200 rounded p-2 shadow-xl z-50 w-56">
              {tooltip}
            </div>
          </div>
        )}
      </div>
      <div className="kpi-value">
        {prefix}{typeof value === 'number' ? value.toLocaleString() : value}{suffix}
      </div>
      {change !== undefined && (
        <div className={`kpi-change ${isPositive ? 'positive' : 'negative'}`}>
          {isPositive ? <ArrowUpRight className="w-4 h-4" /> : <ArrowDownRight className="w-4 h-4" />}
          <span>{Math.abs(change)}%</span>
          {changeLabel && <span className="text-gray-400 font-normal"> {changeLabel}</span>}
        </div>
      )}
    </div>
  );
};
