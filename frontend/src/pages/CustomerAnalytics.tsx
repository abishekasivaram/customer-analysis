import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import KPICard from '../components/KPICard';
import { Users, Clock, Footprints } from 'lucide-react';

export default function CustomerAnalytics() {
  const flowData = [
    { zone: 'Entrance', traffic: 120 },
    { zone: 'Zone A', traffic: 98 },
    { zone: 'Zone B', traffic: 86 },
    { zone: 'Zone C', traffic: 45 },
    { zone: 'Checkout', traffic: 110 },
  ];

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Customer Analytics</h1>
        <p className="text-slate-500 dark:text-slate-400">Foot traffic and journey analysis</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <KPICard title="Total Unique Visitors" value="1,205" trend={12} icon={<Users />} status="good" />
        <KPICard title="Avg Visit Duration" value="14.5 min" trend={-1} icon={<Clock />} status="neutral" />
        <KPICard title="Customer Journeys Tracked" value="1,192" icon={<Footprints />} status="good" />
      </div>

      <div className="card">
        <h3 className="font-semibold text-slate-800 dark:text-white mb-6">Store Flow (Zone Traffic)</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={flowData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis dataKey="zone" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip cursor={{fill: 'transparent'}} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
              <Bar dataKey="traffic" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
