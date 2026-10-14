import React, { useEffect, useState } from 'react';
import KPICard from '../components/KPICard';
import SystemStatus from '../components/SystemStatus';
import { Users, Activity, Target, Zap, AlertTriangle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { fetchAPI } from '../api/config';

const DEFAULT_DASHBOARD_DATA = {
  summary: {
    metrics: {
      customers_total: 33,
      customers: 33,
      total_visitors: 33,
      unique_customers: 33,
      total_tracked_persons: 90,
      total_zone_visits: 75,
      avg_dwell_time: "4.1s",
      avg_dwell_time_seconds: 4.1,
      average_visit_duration: "4.1s",
      overall_conversion_rate: 95.0,
      conversion_rate: "95.0",
      customer_engagement_score: 60.65,
      store_health_score: 100.0,
      total_events: 109,
      total_interactions: 177,
      peak_hour: "14:00",
      peak_shopping_time: "12:00 PM"
    },
    critical_alerts: [
      {
        severity: "HIGH",
        zone: "Zone B",
        message: "High congestion detected in Zone B (28 visitors).",
        description: "High congestion detected in Zone B (28 visitors).",
        recommendation: "Increase staff allocation.",
        alert_type: "Congestion Alert"
      },
      {
        severity: "HIGH",
        zone: "Zone C",
        message: "High congestion detected in Zone C (17 visitors).",
        description: "High congestion detected in Zone C (17 visitors).",
        recommendation: "Increase staff allocation.",
        alert_type: "Congestion Alert"
      },
      {
        severity: "HIGH",
        zone: "Zone D",
        message: "High congestion detected in Zone D (18 visitors).",
        description: "High congestion detected in Zone D (18 visitors).",
        recommendation: "Increase staff allocation.",
        alert_type: "Congestion Alert"
      }
    ],
    traffic_trend: [
      { time: '09:00', traffic: 12, sales: 9 },
      { time: '10:00', traffic: 17, sales: 15 },
      { time: '11:00', traffic: 24, sales: 21 },
      { time: '12:00', traffic: 33, sales: 31 },
      { time: '13:00', traffic: 28, sales: 26 },
      { time: '14:00', traffic: 31, sales: 29 },
      { time: '15:00', traffic: 18, sales: 16 }
    ]
  },
  health: {
    store_health_score: 100,
    status: 'Healthy',
    overall_score: 100
  }
};

export default function ExecutiveDashboard() {
  const [data, setData] = useState<any>(DEFAULT_DASHBOARD_DATA);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        const [summary, health, retailSummary, businessMetrics] = await Promise.all([
          fetchAPI('/advisor/summary'),
          fetchAPI('/advisor/store-health'),
          fetchAPI('/retail/summary'),
          fetchAPI('/retail/metrics')
        ]);

        if (summary || health) {
          setData((prev: any) => ({
            ...prev,
            summary: summary || prev.summary,
            health: health || prev.health,
            retailSummary: retailSummary || prev.retailSummary,
            businessMetrics: businessMetrics || prev.businessMetrics
          }));
        }
      } catch (error) {
        console.warn("Using offline dataset defaults for Executive Dashboard:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading && !data) return <div className="p-8 animate-pulse flex space-x-4">Loading Executive Dashboard...</div>;

  // Extract metrics based on the dataset outputs
  const metrics = data.summary?.metrics || {};
  const retail = data.retailSummary || {};
  const business = data.businessMetrics || {};

  const totalVisitors = 
    metrics.customers_total ||
    metrics.customers ||
    metrics.total_visitors ||
    retail.total_customers ||
    33;

  const rawDwell = 
    metrics.avg_dwell_time ||
    metrics.avg_dwell_time_seconds ||
    retail.average_dwell_time ||
    4.1;

  const avgDwellTime = typeof rawDwell === 'number' 
    ? `${Number(rawDwell).toFixed(1)}s` 
    : String(rawDwell);

  const rawConv = 
    metrics.overall_conversion_rate !== undefined 
      ? metrics.overall_conversion_rate 
      : (business.visit_completion_rate !== undefined ? business.visit_completion_rate * 100 : 95.0);

  const conversionRate = `${Number(rawConv).toFixed(1)}%`;

  const businessScore = 
    data.health?.overall_score || 
    data.health?.store_health_score || 
    metrics.store_health_score || 
    100;

  const chartData = data.summary?.traffic_trend || [
    { time: '09:00', traffic: 12, sales: 9 },
    { time: '10:00', traffic: 17, sales: 15 },
    { time: '11:00', traffic: 24, sales: 21 },
    { time: '12:00', traffic: 33, sales: 31 },
    { time: '13:00', traffic: 28, sales: 26 },
    { time: '14:00', traffic: 31, sales: 29 },
    { time: '15:00', traffic: 18, sales: 16 },
  ];

  const alerts = data.summary?.critical_alerts || data.summary?.alerts || [];

  return (
    <div className="space-y-6 fade-in">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Executive Dashboard</h1>
          <p className="text-slate-500 dark:text-slate-400">Store Performance & AI Summary for Today</p>
        </div>
        <div className="bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 px-4 py-2 rounded-lg font-medium text-sm border border-primary-100 dark:border-primary-800">
          Store Health: {data.health?.store_health_score || 100}/100 ({data.health?.status || 'Healthy'})
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard 
          title="Total Visitors" 
          value={totalVisitors} 
          trend={12} 
          icon={<Users />} 
          status="good" 
          subtitle="33 unique / 90 tracked" 
        />
        <KPICard 
          title="Avg Dwell Time" 
          value={avgDwellTime} 
          trend={-2} 
          icon={<Activity />} 
          status="neutral" 
          subtitle="Across active zones" 
        />
        <KPICard 
          title="Conversion Rate" 
          value={conversionRate} 
          trend={4.5} 
          icon={<Target />} 
          status="good" 
          subtitle="Visit completion rate" 
        />
        <KPICard 
          title="Business Score" 
          value={businessScore} 
          trend={1.2} 
          icon={<Zap />} 
          status="good" 
          subtitle="Outperforming benchmark" 
        />
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
              {alerts.map((a: any, i: number) => (
                <li key={i} className="text-sm p-3 bg-amber-50 dark:bg-amber-900/20 text-amber-800 dark:text-amber-300 rounded-lg border border-amber-200 dark:border-amber-800">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-semibold text-xs uppercase tracking-wider text-amber-700 dark:text-amber-400">
                      {a.zone ? `${a.zone} • ` : ''}{a.severity || 'HIGH'}
                    </span>
                    {a.alert_type && <span className="text-xs opacity-75">{a.alert_type}</span>}
                  </div>
                  <div>{a.message || a.description}</div>
                  {a.recommendation && (
                    <div className="text-xs text-amber-700 dark:text-amber-400 mt-1 font-medium">
                      Action: {a.recommendation}
                    </div>
                  )}
                </li>
              ))}
              {alerts.length === 0 && <li className="text-sm text-slate-500">No critical alerts.</li>}
            </ul>
          </div>
          <SystemStatus />
        </div>
      </div>
    </div>
  );
}
