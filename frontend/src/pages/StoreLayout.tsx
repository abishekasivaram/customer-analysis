import React, { useState } from 'react';
import { Map, Activity, Users, Box } from 'lucide-react';

export default function StoreLayout() {
  const [activeZone, setActiveZone] = useState<string | null>('Zone C');

  const zones = [
    { id: 'Zone A', name: 'Entrance & Fresh Produce', status: 'Healthy', traffic: 'High', color: 'bg-green-500' },
    { id: 'Zone B', name: 'Dairy & Essentials', status: 'Warning', traffic: 'Medium', color: 'bg-yellow-500' },
    { id: 'Zone C', name: 'Premium Goods', status: 'Critical', traffic: 'Low', color: 'bg-red-500' },
    { id: 'Zone D', name: 'Checkout Area', status: 'Warning', traffic: 'High', color: 'bg-yellow-500' },
  ];

  const activeZoneDetails = zones.find(z => z.id === activeZone);

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Interactive Store Layout</h1>
        <p className="text-slate-500 dark:text-slate-400">Live Heatmap & Zone Performance</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Layout Map */}
        <div className="lg:col-span-2 card bg-slate-100 dark:bg-slate-800/50 min-h-[500px] flex items-center justify-center relative overflow-hidden">
          <div className="absolute top-4 left-4 flex gap-2">
            <span className="px-2 py-1 bg-white dark:bg-dark-card rounded text-xs font-medium text-slate-600 shadow-sm flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-green-500"></div> Healthy</span>
            <span className="px-2 py-1 bg-white dark:bg-dark-card rounded text-xs font-medium text-slate-600 shadow-sm flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-yellow-500"></div> Warning</span>
            <span className="px-2 py-1 bg-white dark:bg-dark-card rounded text-xs font-medium text-slate-600 shadow-sm flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-red-500"></div> Critical</span>
          </div>

          {/* Abstract Store Layout */}
          <div className="w-3/4 h-3/4 relative border-4 border-slate-300 dark:border-slate-700 rounded-xl bg-white dark:bg-dark-card p-4 grid grid-cols-2 grid-rows-2 gap-4">
            {zones.map((zone) => (
              <button 
                key={zone.id}
                onClick={() => setActiveZone(zone.id)}
                className={`relative rounded-lg border-2 transition-all ${activeZone === zone.id ? 'border-primary-500 shadow-lg scale-[1.02]' : 'border-transparent hover:border-slate-300 dark:hover:border-slate-600'} bg-slate-50 dark:bg-slate-800 flex items-center justify-center flex-col overflow-hidden group`}
              >
                {/* Heatmap overlay simulation */}
                <div className={`absolute inset-0 opacity-10 ${zone.color}`}></div>
                <div className={`absolute bottom-0 left-0 w-full h-1 ${zone.color}`}></div>
                
                <span className="font-bold text-slate-700 dark:text-slate-200">{zone.id}</span>
                <span className="text-xs text-slate-500 mt-1">{zone.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Zone Details */}
        <div className="space-y-6">
          <div className="card h-full">
            <h3 className="font-semibold text-slate-800 dark:text-white mb-6 border-b border-slate-200 dark:border-slate-700 pb-4 flex justify-between items-center">
              Zone Details
              <span className={`text-xs px-2 py-1 rounded-full text-white ${activeZoneDetails?.color}`}>
                {activeZoneDetails?.status}
              </span>
            </h3>
            
            {activeZone ? (
              <div className="space-y-6 animate-in slide-in-from-right-4">
                <div>
                  <h4 className="text-2xl font-bold text-slate-900 dark:text-white">{activeZoneDetails?.id}</h4>
                  <p className="text-slate-500">{activeZoneDetails?.name}</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
                    <div className="text-xs text-slate-500 mb-1 flex items-center gap-1"><Users className="w-3 h-3"/> Traffic</div>
                    <div className="font-semibold text-slate-900 dark:text-white">{activeZoneDetails?.traffic}</div>
                  </div>
                  <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
                    <div className="text-xs text-slate-500 mb-1 flex items-center gap-1"><Activity className="w-3 h-3"/> Dwell Time</div>
                    <div className="font-semibold text-slate-900 dark:text-white">{activeZoneDetails?.id === 'Zone C' ? 'High' : 'Normal'}</div>
                  </div>
                  <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg col-span-2">
                    <div className="text-xs text-slate-500 mb-1 flex items-center gap-1"><Box className="w-3 h-3"/> Interaction Rate</div>
                    <div className="font-semibold text-slate-900 dark:text-white">{activeZoneDetails?.id === 'Zone C' ? '12% (Poor)' : '45% (Good)'}</div>
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
                  <h5 className="font-medium text-sm text-slate-700 dark:text-slate-300 mb-2">AI Recommendation</h5>
                  <p className="text-sm text-slate-600 dark:text-slate-400 bg-primary-50 dark:bg-primary-900/20 p-3 rounded-lg border border-primary-100 dark:border-primary-800/50">
                    {activeZoneDetails?.id === 'Zone C' 
                      ? "High traffic but low interaction detected. Relocating premium items to eye-level shelves recommended."
                      : "Performance is optimal. Maintain current layout and inventory levels."}
                  </p>
                </div>
              </div>
            ) : (
              <div className="h-48 flex items-center justify-center text-slate-400 text-sm">
                Select a zone to view details
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
