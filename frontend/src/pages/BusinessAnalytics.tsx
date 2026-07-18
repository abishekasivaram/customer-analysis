import React from 'react';
import KPICard from '../components/KPICard';
import { Target, TrendingUp, DollarSign } from 'lucide-react';

export default function BusinessAnalytics() {
  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Business Analytics</h1>
        <p className="text-slate-500 dark:text-slate-400">Conversion funnels and KPIs</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <KPICard title="Total Engagement Rate" value="38.5%" trend={2.1} icon={<TrendingUp />} status="good" />
        <KPICard title="Sales Conversion Rate" value="14.2%" trend={-0.5} icon={<Target />} status="warning" />
        <KPICard title="Estimated Value Generation" value="$12,450" icon={<DollarSign />} status="good" />
      </div>

      <div className="card">
        <h3 className="font-semibold text-slate-800 dark:text-white mb-6">Store Conversion Funnel</h3>
        <div className="flex flex-col space-y-4">
          <FunnelStep label="Total Visitors" value={1205} percentage={100} color="bg-blue-500" />
          <FunnelStep label="Zone Entry (Engaged)" value={890} percentage={73.8} color="bg-indigo-500" />
          <FunnelStep label="Product Interaction" value={450} percentage={37.3} color="bg-purple-500" />
          <FunnelStep label="Conversion (Kept Item)" value={150} percentage={12.4} color="bg-green-500" />
        </div>
      </div>
    </div>
  );
}

function FunnelStep({ label, value, percentage, color }: { label: string, value: number, percentage: number, color: string }) {
  return (
    <div className="flex items-center gap-4">
      <div className="w-48 text-right text-sm font-medium text-slate-600 dark:text-slate-400">{label}</div>
      <div className="flex-1 bg-slate-100 dark:bg-slate-800 rounded-full h-8 flex items-center overflow-hidden">
        <div className={`h-full ${color} flex items-center px-4 text-xs font-bold text-white transition-all`} style={{ width: `${percentage}%` }}>
          {percentage}%
        </div>
      </div>
      <div className="w-16 font-bold text-slate-900 dark:text-white">{value}</div>
    </div>
  );
}
