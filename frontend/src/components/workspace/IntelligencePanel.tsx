import React, { useState } from 'react';
import { Lightbulb, MessageSquare, ShieldAlert, ArrowRight, User } from 'lucide-react';
import { useTimeline } from '../../contexts/TimelineContext';

export default function IntelligencePanel() {
  const { selectedCustomerId, setSeekTo, setIsPlaying } = useTimeline();
  const [activeTab, setActiveTab] = useState<'recommendations' | 'ask_ai'>('recommendations');
  const [query, setQuery] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    setIsLoading(true);
    try {
      const res = await fetch('http://localhost:8000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      setAiResponse(data.response);
    } catch (e) {
      setAiResponse("Failed to connect to AI engine.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-dark-card rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col h-[400px]">
      <div className="flex border-b border-slate-200 dark:border-slate-800">
        <button 
          className={`flex-1 py-3 text-xs font-semibold border-b-2 flex items-center justify-center gap-2 ${activeTab === 'recommendations' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-slate-500'}`}
          onClick={() => setActiveTab('recommendations')}
        ><Lightbulb className="w-4 h-4"/> AI Evidence Viewer</button>
        <button 
          className={`flex-1 py-3 text-xs font-semibold border-b-2 flex items-center justify-center gap-2 ${activeTab === 'ask_ai' ? 'border-primary-500 text-primary-600 dark:text-primary-400' : 'border-transparent text-slate-500'}`}
          onClick={() => setActiveTab('ask_ai')}
        ><MessageSquare className="w-4 h-4"/> Ask Retail AI</button>
      </div>

      <div className="flex-1 overflow-y-auto p-3 custom-scrollbar">
        {selectedCustomerId && (
          <div className="mb-4 bg-primary-50 dark:bg-primary-900/20 p-3 rounded-lg border border-primary-100 dark:border-primary-800/50">
            <h4 className="text-xs font-bold text-primary-700 dark:text-primary-400 flex items-center gap-1 mb-1">
              <User className="w-3 h-3" /> Customer Inspector (ID: {selectedCustomerId})
            </h4>
            <p className="text-[10px] text-primary-600 dark:text-primary-500 mb-2">Customer journey isolated. Interactions synchronized with video.</p>
            <div className="flex gap-2">
              <span className="px-2 py-0.5 bg-white dark:bg-dark-bg rounded text-[10px] font-medium text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700">High Purchase Intent</span>
              <span className="px-2 py-0.5 bg-white dark:bg-dark-bg rounded text-[10px] font-medium text-slate-600 dark:text-slate-400 border border-slate-200 dark:border-slate-700">Zone C</span>
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="flex flex-col gap-3">
            <div className="p-3 border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-900/10 rounded-lg">
              <div className="flex items-start gap-2 mb-2">
                <ShieldAlert className="w-4 h-4 text-red-500 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-slate-800 dark:text-white">Relocate Premium Products to Zone C</h4>
                  <span className="text-[10px] font-bold text-red-600 dark:text-red-400 uppercase tracking-wide">High Priority</span>
                </div>
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-300 mb-3">
                High traffic detected in Zone C but low product interaction. Relocating premium products could increase engagement by 12%.
              </p>
              <div className="flex justify-between items-center text-xs text-slate-500 mb-3">
                <span className="font-mono">Confidence: 92%</span>
                <span className="font-mono text-green-600 dark:text-green-400">ROI: +12%</span>
              </div>
              <button 
                onClick={() => { setSeekTo(45); setIsPlaying(false); }}
                className="w-full py-1.5 bg-white dark:bg-dark-bg border border-slate-200 dark:border-slate-700 rounded text-xs font-medium text-slate-700 dark:text-slate-300 hover:border-primary-500 transition-colors"
              >
                View Evidence in Video
              </button>
            </div>
            
            <div className="p-3 border border-yellow-200 dark:border-yellow-900/50 bg-yellow-50 dark:bg-yellow-900/10 rounded-lg">
              <div className="flex items-start gap-2 mb-2">
                <Lightbulb className="w-4 h-4 text-yellow-500 mt-0.5" />
                <div>
                  <h4 className="text-sm font-semibold text-slate-800 dark:text-white">Improve Shelf Visibility in Zone B</h4>
                  <span className="text-[10px] font-bold text-yellow-600 dark:text-yellow-400 uppercase tracking-wide">Medium Priority</span>
                </div>
              </div>
              <p className="text-xs text-slate-600 dark:text-slate-300 mb-3">
                Products in Zone B have lower visibility. Rearranging shelves can improve interaction by 8%.
              </p>
              <button 
                onClick={() => { setSeekTo(15); setIsPlaying(false); }}
                className="w-full py-1.5 bg-white dark:bg-dark-bg border border-slate-200 dark:border-slate-700 rounded text-xs font-medium text-slate-700 dark:text-slate-300 hover:border-primary-500 transition-colors"
              >
                View Evidence in Video
              </button>
            </div>
          </div>
        )}

        {activeTab === 'ask_ai' && (
          <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto mb-3">
              {aiResponse ? (
                <div className="bg-slate-100 dark:bg-slate-800 rounded-lg p-3 text-sm text-slate-700 dark:text-slate-300">
                  {aiResponse}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-slate-500 opacity-50 space-y-2">
                  <MessageSquare className="w-8 h-8" />
                  <p className="text-xs text-center">Ask a question about the video or analytics data.</p>
                </div>
              )}
            </div>
            <form onSubmit={handleAsk} className="flex gap-2">
              <input 
                type="text" 
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Ask Retail AI..." 
                className="flex-1 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:text-white"
                disabled={isLoading}
              />
              <button 
                type="submit" 
                disabled={isLoading}
                className="bg-primary-600 hover:bg-primary-700 text-white p-2 rounded-lg transition-colors flex items-center justify-center"
              >
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
