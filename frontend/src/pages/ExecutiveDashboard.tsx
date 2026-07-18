import React, { useEffect, useState } from 'react';
import KPICard from '../components/KPICard';
import SystemStatus from '../components/SystemStatus';
import { Users, Activity, Target, Zap, AlertTriangle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { fetchAPI } from '../api/config';

export default function ExecutiveDashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const summary = await fetchAPI('/advisor/summary');
        const health = await fetchAPI('/advisor/store-health');
        if (summary && health) {
          setData({ summary, health });
        } else {
          setData(null);
        }
      } catch (error) {
        console.error("Failed to load dashboard data", error);
        setData(null);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const chartData = [
    { time: '09:00', traffic: 40, sales: 24 },
    { time: '10:00', traffic: 30, sales: 13 },
    { time: '11:00', traffic: 20, sales: 98 },
    { time: '12:00', traffic: 90, sales: 39 },
    { time: '13:00', traffic: 110, sales: 48 },
    { time: '14:00', traffic: 85, sales: 38 },
    { time: '15:00', traffic: 130, sales: 43 },
  ];

  if (loading) return <div className="p-8 animate-pulse flex space-x-4">Loading Executive Dashboard...</div>;
  if (!data) return <div className="p-8 text-slate-500">No data available or backend is not reachable.</div>;

  return (
    <div className="space-y-6 fade-in">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Executive Dashboard</h1>
          <p className="text-slate-500 dark:text-slate-400">Store Performance & AI Summary for Today</p>
        </div>
        <div className="bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 px-4 py-2 rounded-lg font-medium text-sm border border-primary-100 dark:border-primary-800">
          Store Health: {data.health.store_health_score}/100 ({data.health.status})
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard title="Total Visitors" value={data.summary.metrics?.customers_total || data.summary.metrics?.customers || 0} trend={12} icon={<Users />} status="good" />
        <KPICard title="Avg Dwell Time" value={data.summary.metrics?.avg_dwell_time_seconds || data.summary.metrics?.avg_dwell_time || 0} trend={-2} icon={<Activity />} status="neutral" />
        <KPICard title="Conversion Rate" value={`${(data.summary.metrics?.overall_conversion_rate || parseFloat(data.summary.metrics?.conversion_rate || '0')).toFixed(1)}%`} trend={4.5} icon={<Target />} status="good" />
        <KPICard title="Business Score" value={data.health.overall_score || data.health.store_health_score || 0} trend={1.2} icon={<Zap />} status="good" subtitle="Outperforming benchmark" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Chart */}
        <div className="lg:col-span-2 card">
          <h3 className="font-semibold text-slate-800 dark:text-white mb-6">Today's Traffic & Engagement Trend</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorTraffic" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="time" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                <Area type="monotone" dataKey="traffic" stroke="#22c55e" strokeWidth={3} fillOpacity={1} fill="url(#colorTraffic)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Side Panels */}
        <div className="space-y-6">
          <div className="card">
            <h3 className="font-semibold text-slate-800 dark:text-white flex items-center gap-2 mb-4">
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              Critical Alerts
            </h3>
            <ul className="space-y-3">
              {(data.summary.critical_alerts || data.summary.alerts || []).map((a: any, i: number) => (
                <li key={i} className="text-sm p-3 bg-amber-50 dark:bg-amber-900/20 text-amber-800 dark:text-amber-300 rounded-lg border border-amber-200 dark:border-amber-800">
                  {a.message || a.alert_type}
                </li>
              ))}
              {(data.summary.critical_alerts || data.summary.alerts || []).length === 0 && <li className="text-sm text-slate-500">No critical alerts.</li>}
            </ul>
          </div>
          <SystemStatus />
        </div>
      </div>
    </div>
  );
}
