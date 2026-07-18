import React from 'react';
import { useTimeline } from '../../contexts/TimelineContext';

export default function InteractiveHeatmap() {
  const { currentVideoTime } = useTimeline();

  // Simple animation using CSS filters to simulate live heatmap changes based on video time
  const hueRotate = Math.floor(currentVideoTime * 5) % 360;
  const opacity = 0.5 + (Math.sin(currentVideoTime / 5) * 0.3);

  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-sm font-semibold text-slate-800 dark:text-white">Live Heatmap (Store Layout)</h3>
        <div className="text-xs text-slate-500 font-mono">Time Sync: Active</div>
      </div>
      
      <div className="flex-1 bg-slate-900 rounded-lg relative overflow-hidden flex items-center justify-center min-h-[250px] border border-slate-800">
        <div 
          className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&q=80&w=800')] bg-cover bg-center opacity-30 mix-blend-luminosity"
        />
        
        {/* Heatmap Overlays */}
        <div className="absolute inset-0" style={{ filter: `hue-rotate(${hueRotate}deg)` }}>
          <div className="absolute top-1/4 left-1/4 w-32 h-32 bg-red-500 rounded-full blur-3xl" style={{ opacity }} />
          <div className="absolute top-1/2 left-1/2 w-48 h-48 bg-yellow-500 rounded-full blur-3xl" style={{ opacity: opacity * 0.8 }} />
          <div className="absolute bottom-1/4 right-1/4 w-40 h-40 bg-green-500 rounded-full blur-3xl opacity-40" />
          <div className="absolute top-1/3 right-1/3 w-24 h-24 bg-blue-500 rounded-full blur-2xl opacity-60" />
        </div>

        {/* Zones */}
        <div className="absolute top-[20%] left-[20%] border border-green-500/50 bg-green-500/10 rounded px-2 py-1 backdrop-blur-sm shadow-lg">
          <div className="text-[10px] font-bold text-white drop-shadow">Zone A (Good)</div>
        </div>
        <div className="absolute top-[20%] right-[30%] border border-yellow-500/50 bg-yellow-500/10 rounded px-2 py-1 backdrop-blur-sm shadow-lg">
          <div className="text-[10px] font-bold text-white drop-shadow">Zone B (Moderate)</div>
        </div>
        <div className="absolute bottom-[30%] left-[25%] border border-red-500/50 bg-red-500/10 rounded px-2 py-1 backdrop-blur-sm shadow-lg z-10">
          <div className="text-[10px] font-bold text-white drop-shadow">Zone C (High Traffic)</div>
        </div>
        
        <div className="absolute bottom-4 right-4 flex flex-col items-center">
          <span className="text-[10px] text-white mb-1">High</span>
          <div className="w-2 h-24 rounded-full bg-gradient-to-t from-blue-500 via-green-500 and-yellow-500 to-red-500" />
          <span className="text-[10px] text-white mt-1">Low</span>
        </div>
      </div>
    </div>
  );
}
