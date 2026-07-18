import React, { useState, useEffect, useRef } from 'react';
import { UploadCloud, CheckCircle2, Play, Pause, Trash2, Activity, Settings2, Loader2, ArrowRight } from 'lucide-react';
import { API_BASE_URL } from '../../api/config';
import { useTimeline } from '../../contexts/TimelineContext';

interface Job {
  session_id: string;
  video_name: string;
  upload_time: number;
  current_stage: string;
  progress: number;
  status: string;
  stages: string[];
}

export default function ProcessingSessionManager() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { activeSessionId, setActiveSessionId } = useTimeline();

  const fetchJobs = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/jobs`);
      if (res.ok) {
        const data = await res.json();
        setJobs(data.jobs);
      }
    } catch (e) {
      console.error('Failed to fetch jobs', e);
    }
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    setIsUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const res = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });
      if (res.ok) {
        const data = await res.json();
        if (data.session_id) setActiveSessionId(data.session_id);
        fetchJobs();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleAction = async (sessionId: string, action: string) => {
    try {
      await fetch(`${API_BASE_URL}/jobs/${sessionId}/${action}`, { method: action === 'cancel' || action === 'resume' ? 'POST' : 'DELETE' });
      fetchJobs();
    } catch (e) {}
  };

  return (
    <div className="bg-white dark:bg-dark-card rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col">
      <div className="p-4 border-b border-slate-200 dark:border-slate-800">
        <h2 className="text-lg font-semibold text-slate-800 dark:text-white flex items-center gap-2">
          <Settings2 className="w-5 h-5 text-primary-500" /> Processing Session Manager
        </h2>
      </div>

      <div className="p-4 flex flex-col gap-4">
        {/* Upload Zone */}
        <div 
          className="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-xl p-6 flex flex-col items-center justify-center text-center cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
          onClick={() => fileInputRef.current?.click()}
        >
          <input type="file" ref={fileInputRef} className="hidden" accept="video/*" onChange={handleUpload} />
          {isUploading ? (
            <Loader2 className="w-8 h-8 text-primary-500 animate-spin mb-2" />
          ) : (
            <UploadCloud className="w-8 h-8 text-slate-400 mb-2" />
          )}
          <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
            {isUploading ? 'Uploading...' : 'Drag & Drop Video Here'}
          </p>
          <p className="text-xs text-slate-500 mt-1">Supports MP4, AVI, MOV (Max 2GB)</p>
          {!isUploading && (
            <button className="mt-3 px-4 py-1.5 bg-primary-600 hover:bg-primary-700 text-white text-xs font-medium rounded-lg">
              Browse Files
            </button>
          )}
        </div>

        {/* Job Queue */}
        <div className="flex flex-col gap-3">
          {jobs.length === 0 && (
            <div className="text-center py-4 text-slate-500 text-sm">No active sessions.</div>
          )}
          {jobs.map(job => (
            <div 
              key={job.session_id} 
              className={`rounded-lg p-3 border cursor-pointer transition-colors ${
                activeSessionId === job.session_id 
                  ? 'bg-primary-50 border-primary-200 dark:bg-primary-900/20 dark:border-primary-800' 
                  : 'bg-slate-50 border-slate-200 dark:bg-slate-800/50 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
              onClick={() => setActiveSessionId(job.session_id)}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Activity className="w-4 h-4 text-primary-500" />
                  <span className="text-sm font-medium text-slate-800 dark:text-white truncate max-w-[150px]" title={job.video_name}>
                    {job.video_name}
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  {job.status === 'Running' && (
                    <button onClick={() => handleAction(job.session_id, 'cancel')} className="p-1 hover:bg-slate-200 dark:hover:bg-slate-700 rounded text-slate-500 hover:text-red-500" title="Pause/Cancel">
                      <Pause className="w-4 h-4" />
                    </button>
                  )}
                  {job.status === 'Cancelled' && (
                    <button onClick={() => handleAction(job.session_id, 'resume')} className="p-1 hover:bg-slate-200 dark:hover:bg-slate-700 rounded text-slate-500 hover:text-green-500" title="Resume">
                      <Play className="w-4 h-4" />
                    </button>
                  )}
                  <button onClick={() => handleAction(job.session_id, '')} className="p-1 hover:bg-slate-200 dark:hover:bg-slate-700 rounded text-slate-500 hover:text-red-500" title="Delete">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                <span>{job.status === 'Completed' ? 'Completed' : job.current_stage}</span>
                <span className="font-mono">{job.progress.toFixed(0)}%</span>
              </div>
              
              <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden mb-3">
                <div 
                  className={`h-full ${job.status === 'Completed' ? 'bg-green-500' : job.status === 'Cancelled' ? 'bg-amber-500' : 'bg-primary-500'} transition-all duration-300`}
                  style={{ width: `${job.progress}%` }}
                />
              </div>

              {/* Animated Pipeline Viz */}
              <div className="flex items-center justify-between gap-1 overflow-x-auto hide-scrollbar pb-1">
                {job.stages.slice(0, 5).map((stage, idx) => {
                  const stageIndex = job.stages.indexOf(job.current_stage);
                  const isPast = idx < stageIndex || job.status === 'Completed';
                  const isCurrent = idx === stageIndex && job.status === 'Running';
                  return (
                    <React.Fragment key={stage}>
                      <div className={`flex flex-col items-center flex-shrink-0 ${isPast ? 'text-green-500' : isCurrent ? 'text-primary-500' : 'text-slate-400'}`}>
                        {isPast ? <CheckCircle2 className="w-4 h-4 mb-0.5" /> : <div className={`w-4 h-4 rounded-full border-2 mb-0.5 ${isCurrent ? 'border-primary-500 bg-primary-100 animate-pulse' : 'border-slate-300 dark:border-slate-600'}`} />}
                        <span className="text-[9px] text-center w-12 truncate leading-tight" title={stage}>{stage}</span>
                      </div>
                      {idx < 4 && <ArrowRight className={`w-3 h-3 flex-shrink-0 ${isPast ? 'text-green-500' : 'text-slate-300 dark:text-slate-700'}`} />}
                    </React.Fragment>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
