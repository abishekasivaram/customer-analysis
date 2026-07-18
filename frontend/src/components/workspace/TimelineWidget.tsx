import React, { useEffect, useState } from 'react';
import { useTimeline } from '../../contexts/TimelineContext';
import { Clock, User, Activity, Map, ArrowRight } from 'lucide-react';
import { API_BASE_URL } from '../../api/config';

interface Event {
  timestamp: string;
  time_sec: number;
  customer_id: number;
  event: string;
  zone: string;
}

export default function TimelineWidget() {
  const { activeSessionId, currentVideoTime, setSeekTo, setIsPlaying, setSelectedCustomerId } = useTimeline();
  const [events, setEvents] = useState<Event[]>([]);
  const [activeTab, setActiveTab] = useState<'timeline'|'customers'|'behaviors'|'zones'>('timeline');

  useEffect(() => {
    if (!activeSessionId) return;
    
    // Poll the timeline data periodically while the video is playing or just once
    const fetchTimeline = () => {
      fetch(`${API_BASE_URL}/timeline/${activeSessionId}`)
        .then(res => {
          if (!res.ok) throw new Error("Timeline not found");
          return res.json();
        })
        .then(data => {
          if (data.events) setEvents(data.events);
        })
        .catch(console.error);
    };
    
    fetchTimeline();
    const interval = setInterval(fetchTimeline, 5000);
    return () => clearInterval(interval);
  }, [activeSessionId]);

  const handleEventClick = (timeSec: number, customerId: number) => {
    setSeekTo(timeSec);
    setIsPlaying(false);
    setSelectedCustomerId(customerId);
  };

  return (
    <div className="bg-white dark:bg-dark-card rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col h-[400px]">
      {/* Tabs */}
      <div className="flex border-b border-slate-200 dark:border-slate-800">
        <button 
          className={`flex-1 py-3 text-xs font-semibold border-b-2 ${activeTab === 'timeline' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'}`}
          onClick={() => setActiveTab('timeline')}
        >Event Timeline</button>
        <button 
          className={`flex-1 py-3 text-xs font-semibold border-b-2 ${activeTab === 'customers' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'}`}
          onClick={() => setActiveTab('customers')}
        >Customers</button>
        <button 
          className={`flex-1 py-3 text-xs font-semibold border-b-2 ${activeTab === 'behaviors' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300'}`}
          onClick={() => setActiveTab('behaviors')}
        >Behaviors</button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-2 custom-scrollbar">
        {activeTab === 'timeline' && (
          <div className="flex flex-col gap-1">
            {events.map((evt, idx) => {
              const isActive = Math.abs(currentVideoTime - evt.time_sec) < 5;
              const isPast = currentVideoTime >= evt.time_sec;
              return (
                <div 
                  key={idx}
                  onClick={() => handleEventClick(evt.time_sec, evt.customer_id)}
                  className={`flex items-start gap-3 p-2 rounded-lg cursor-pointer transition-colors ${
                    isActive ? 'bg-primary-50 dark:bg-primary-900/20 border border-primary-100 dark:border-primary-800/50' 
                             : 'hover:bg-slate-50 dark:hover:bg-slate-800/50 border border-transparent'
                  }`}
                >
                  <div className={`text-xs font-mono font-medium pt-1 ${isActive ? 'text-primary-600 dark:text-primary-400' : isPast ? 'text-slate-600 dark:text-slate-400' : 'text-slate-400 dark:text-slate-500'}`}>
                    {evt.timestamp}
                  </div>
                  
                  <div className="relative flex flex-col items-center">
                    <div className={`w-2 h-2 rounded-full mt-1.5 ${isActive ? 'bg-primary-500 shadow-[0_0_8px_rgba(59,130,246,0.8)]' : isPast ? 'bg-green-500' : 'bg-slate-300 dark:bg-slate-600'}`} />
                    {idx < events.length - 1 && (
                      <div className={`w-0.5 h-full absolute top-4 ${isPast ? 'bg-green-500/50' : 'bg-slate-200 dark:bg-slate-700'}`} />
                    )}
                  </div>
                  
                  <div className="flex-1 pb-2">
                    <div className="flex items-center justify-between">
                      <span className={`text-sm font-semibold ${isActive ? 'text-slate-900 dark:text-white' : 'text-slate-700 dark:text-slate-300'}`}>
                        {evt.event}
                      </span>
                      <span className="text-[10px] font-medium px-2 py-0.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 rounded">
                        {evt.zone}
                      </span>
                    </div>
                    <div className="text-xs text-slate-500 flex items-center gap-1 mt-1">
                      <User className="w-3 h-3" /> Customer ID: {evt.customer_id}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
        {activeTab !== 'timeline' && (
          <div className="h-full flex flex-col items-center justify-center text-slate-500">
            <Activity className="w-8 h-8 mb-2 opacity-50" />
            <p className="text-sm">Select Event Timeline</p>
          </div>
        )}
      </div>
      
      <div className="p-2 border-t border-slate-200 dark:border-slate-800">
         <button className="w-full text-xs font-medium text-primary-600 dark:text-primary-400 hover:underline flex items-center justify-center gap-1">
           View Full Timeline <ArrowRight className="w-3 h-3" />
         </button>
      </div>
    </div>
  );
}
