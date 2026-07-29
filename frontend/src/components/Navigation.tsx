import React from 'react';
import { 
  BarChart3, 
  PieChart, 
  TrendingDown, 
  Users, 
  Trophy, 
  Building2, 
  Globe,
  Leaf
} from 'lucide-react';

interface NavigationProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const TABS = [
  { id: 'overview', label: '1. Executive Overview', icon: BarChart3 },
  { id: 'revenue', label: '2. Revenue Engine', icon: PieChart },
  { id: 'costs', label: '3. Cost & Efficiency', icon: TrendingDown },
  { id: 'squad', label: '4. Squad Economics', icon: Users },
  { id: 'sporting-roi', label: '5. Sporting ROI', icon: Trophy },
  { id: 'stadium', label: '6. Bernabéu & Risk', icon: Building2 },
  { id: 'benchmark', label: '7. European Benchmark', icon: Globe },
  { id: 'esg-femenino', label: '8. ESG & Femenino', icon: Leaf },
];

export const Navigation: React.FC<NavigationProps> = ({ activeTab, setActiveTab }) => {
  return (
    <nav className="nav-tabs">
      {TABS.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`nav-tab ${isActive ? 'active' : ''}`}
          >
            <Icon className="w-4 h-4" />
            <span>{tab.label}</span>
          </button>
        );
      })}
    </nav>
  );
};
