import React from 'react';
import { Activity, Database, Server, ShieldCheck } from 'lucide-react';

export default function SystemStatus() {
  const statuses = [
    { name: 'Backend API', status: 'Operational', icon: Server },
    { name: 'Analytics Engine', status: 'Operational', icon: Activity },
    { name: 'Recommendation Engine', status: 'Operational', icon: LightbulbIcon },
    { name: 'Dataset Connection', status: 'Operational', icon: Database },
  ];

  return (
    <div className="card">
      <h3 className="font-semibold text-slate-800 dark:text-white flex items-center gap-2 mb-4">
        <ShieldCheck className="w-5 h-5 text-green-500" />
        Live System Status
      </h3>
      <div className="space-y-3">
        {statuses.map((s, i) => (
          <div key={i} className="flex items-center justify-between">
            <div className="flex items-center gap-3 text-sm text-slate-600 dark:text-slate-400">
              <s.icon className="w-4 h-4" />
              {s.name}
            </div>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">{s.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function LightbulbIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1.3.5 2.6 1.5 3.5.8.8 1.3 1.5 1.5 2.5" />
      <path d="M9 18h6" />
      <path d="M10 22h4" />
    </svg>
  );
}
