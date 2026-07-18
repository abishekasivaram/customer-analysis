import React from 'react';
import { TimelineProvider } from '../contexts/TimelineContext';
import ProcessingSessionManager from '../components/workspace/ProcessingSessionManager';
import EnterpriseVideoPlayer from '../components/workspace/EnterpriseVideoPlayer';
import TimelineWidget from '../components/workspace/TimelineWidget';
import LiveKPIDashboard from '../components/workspace/LiveKPIDashboard';
import IntelligencePanel from '../components/workspace/IntelligencePanel';
import InteractiveHeatmap from '../components/workspace/InteractiveHeatmap';
import { ShieldAlert, PlayCircle, Database } from 'lucide-react';

export default function VideoWorkspace() {
  return (
    <TimelineProvider>
      <div className="flex flex-col h-full space-y-4">
        {/* Top Bar / Header context */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-800 dark:text-white flex items-center gap-2">
              <PlayCircle className="text-primary-500 w-6 h-6"/>
              AI Video Intelligence Workspace
            </h1>
            <p className="text-slate-500 text-sm mt-1">Enterprise Video Analysis & Real-Time Intelligence</p>
          </div>
          <div className="flex items-center gap-3">
            <span className="px-3 py-1 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 text-xs font-bold uppercase rounded-full flex items-center gap-1">
              <Database className="w-3 h-3" /> Live Backend Connected
            </span>
          </div>
        </div>

        {/* 3-Column Enterprise Dashboard Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 flex-1 min-h-0">
          
          {/* Left Column: Processing & Jobs (col-span-3) */}
          <div className="lg:col-span-3 flex flex-col gap-4 overflow-y-auto pr-1 custom-scrollbar">
            <ProcessingSessionManager />
            <LiveKPIDashboard />
          </div>

          {/* Center Column: Video & Spatial Analytics (col-span-6) */}
          <div className="lg:col-span-6 flex flex-col gap-4 overflow-y-auto pr-1 custom-scrollbar">
            <div className="bg-white dark:bg-dark-card rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden flex flex-col h-[55%] min-h-[400px]">
              <EnterpriseVideoPlayer />
            </div>
            
            <div className="bg-white dark:bg-dark-card rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-4 flex-1">
              <InteractiveHeatmap />
            </div>
          </div>

          {/* Right Column: Intelligence & Timelines (col-span-3) */}
          <div className="lg:col-span-3 flex flex-col gap-4 overflow-y-auto pr-1 custom-scrollbar">
            <IntelligencePanel />
            <TimelineWidget />
          </div>
          
        </div>
      </div>
    </TimelineProvider>
  );
}
