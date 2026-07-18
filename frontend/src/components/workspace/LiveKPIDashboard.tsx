import React, { useState, useEffect } from 'react';
import { useTimeline } from '../../contexts/TimelineContext';
import { Users, Activity, ShoppingBag, TrendingUp, ShieldCheck } from 'lucide-react';
import { API_BASE_URL } from '../../api/config';

export default function LiveKPIDashboard() {
  const { activeSessionId } = useTimeline();
  
  const [data, setData] = useState({
    people: 0,
    interactions: 0,
    pickups: 0,
    intent: 0,
    storeHealth: 0,
    businessScore: 0
  });

  useEffect(() => {
    if (!activeSessionId) return;
    
    let interval: NodeJS.Timeout;
    
    const fetchKPIs = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/summary/${activeSessionId}`);
        if (!res.ok) return;
        const data = await res.json();
        
        if (data && data.people !== undefined) {
          setData({
            people: data.people,
            interactions: data.interactions,
            pickups: data.pickups,
            intent: data.intent,
            storeHealth: data.storeHealth || 85,
            businessScore: data.businessScore || 82
          });
        }
      } catch (e) {
        console.error("Failed to fetch KPIs:", e);
      }
    };

    fetchKPIs();
    interval = setInterval(fetchKPIs, 5000);
    return () => clearInterval(interval);
  }, [activeSessionId]);
  
  const kpis = [
    { title: "People Detected", value: data.people, icon: Users, color: "text-blue-500", bg: "bg-blue-100 dark:bg-blue-900/30", trend: "+18%" },
    { title: "Interactions", value: data.interactions, icon: Activity, color: "text-indigo-500", bg: "bg-indigo-100 dark:bg-indigo-900/30", trend: "+24%" },
    { title: "Pickups", value: data.pickups, icon: ShoppingBag, color: "text-amber-500", bg: "bg-amber-100 dark:bg-amber-900/30", trend: "+12%" },
    { title: "Purchase Intent", value: data.intent, icon: TrendingUp, color: "text-rose-500", bg: "bg-rose-100 dark:bg-rose-900/30", trend: "+8%" }
  ];

  return (
    <div className="bg-white dark:bg-dark-card rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-4">
      <h3 className="text-sm font-semibold text-slate-800 dark:text-white mb-3">Live Intelligence KPIs</h3>
      <div className="grid grid-cols-2 gap-3">
        {kpis.map((kpi, idx) => (
          <div key={idx} className="bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg border border-slate-100 dark:border-slate-700">
            <div className="flex items-start justify-between mb-2">
              <div className={`p-1.5 rounded-lg ${kpi.bg}`}>
                <kpi.icon className={`w-4 h-4 ${kpi.color}`} />
              </div>
              <span className="text-xs font-medium text-green-600 dark:text-green-400">{kpi.trend}</span>
            </div>
            <div className="text-2xl font-bold text-slate-800 dark:text-white leading-tight">
              {kpi.value.toLocaleString()}
            </div>
            <div className="text-[10px] font-medium text-slate-500 mt-0.5 truncate">
              {kpi.title}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 p-3 bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 rounded-lg border border-emerald-100 dark:border-emerald-800/30 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-emerald-100 dark:bg-emerald-800/50 flex items-center justify-center">
            <ShieldCheck className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div>
            <div className="text-xs font-semibold text-emerald-800 dark:text-emerald-300">Store Health Score</div>
            <div className="text-lg font-bold text-emerald-600 dark:text-emerald-400">{data.storeHealth || '--'}<span className="text-xs font-normal opacity-70">/100</span></div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-xs font-semibold text-slate-800 dark:text-slate-200">Business Score</div>
          <div className="text-lg font-bold text-slate-800 dark:text-white">{data.businessScore || '--'}<span className="text-xs font-normal opacity-70">/100</span></div>
        </div>
      </div>
    </div>
  );
}
