import React, { useEffect, useState } from 'react';
import { Lightbulb, TrendingUp, CheckCircle, Clock } from 'lucide-react';
import { fetchAPI } from '../api/config';
import { cn } from '../lib/utils';

export default function AIAdvisorDashboard() {
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      const recs = await fetchAPI('/advisor/recommendations');
      if (recs) {
        setRecommendations(recs);
      } else {
        // Mock fallback if API fails
        setRecommendations([
          {
            recommendation_id: 'REC-001',
            title: 'Relocate Premium Products to High Traffic Zone',
            category: 'Layout Optimization',
            priority: 'HIGH',
            confidence: 92,
            description: 'Zone C experiences high customer traffic but relatively low product interaction. Relocating premium products and improving shelf visibility could increase engagement.',
            business_impact: 'High',
            expected_roi: 'Increase conversion by 12%',
            triggered_rule: 'low_engagement_high_traffic'
          }
        ]);
      }
      setLoading(false);
    }
    loadData();
  }, []);

  if (loading) return <div className="p-8 animate-pulse">Loading AI Advisor...</div>;

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">AI Business Advisor</h1>
        <p className="text-slate-500 dark:text-slate-400">Heuristic Engine Recommendations & Insights</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {recommendations.map((rec) => (
          <div key={rec.recommendation_id} className="card relative overflow-hidden border-l-4" style={{ borderLeftColor: getPriorityColor(rec.priority) }}>
            <div className="absolute top-6 right-6">
              <span className={cn(
                "px-3 py-1 text-xs font-bold rounded-full uppercase tracking-wider",
                rec.priority === 'HIGH' || rec.priority === 'CRITICAL' ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400" :
                rec.priority === 'MEDIUM' ? "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400" :
                "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
              )}>
                {rec.priority} PRIORITY
              </span>
            </div>
            
            <div className="flex items-start gap-4 pr-32">
              <div className="p-3 bg-primary-50 dark:bg-primary-900/20 text-primary-600 rounded-xl">
                <Lightbulb className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-2">{rec.title}</h3>
                <p className="text-slate-600 dark:text-slate-300 mb-6 leading-relaxed">
                  <strong className="font-semibold text-slate-800 dark:text-slate-200">Business Interpretation: </strong> 
                  {rec.description}
                </p>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                    <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 flex items-center gap-1"><TargetIcon/> Confidence</div>
                    <div className="font-bold text-lg text-slate-900 dark:text-white">{rec.confidence}%</div>
                  </div>
                  <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
                    <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 flex items-center gap-1"><TrendingUp className="w-3 h-3"/> Impact</div>
                    <div className="font-bold text-lg text-slate-900 dark:text-white">{rec.business_impact}</div>
                  </div>
                  <div className="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg col-span-2">
                    <div className="text-xs text-slate-500 dark:text-slate-400 mb-1 flex items-center gap-1"><CheckCircle className="w-3 h-3"/> Expected ROI</div>
                    <div className="font-bold text-lg text-slate-900 dark:text-white">{rec.expected_roi}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
        {recommendations.length === 0 && (
          <div className="text-center p-12 card text-slate-500">
            No recommendations generated at this time.
          </div>
        )}
      </div>
    </div>
  );
}

function TargetIcon() {
  return <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>;
}

function getPriorityColor(priority: string) {
  switch(priority?.toUpperCase()) {
    case 'CRITICAL': return '#ef4444';
    case 'HIGH': return '#f97316';
    case 'MEDIUM': return '#eab308';
    default: return '#3b82f6';
  }
}
