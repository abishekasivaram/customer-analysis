import React, { useRef, useEffect, useState } from 'react';
import { useTimeline } from '../../contexts/TimelineContext';
import { Play, Pause, Maximize, SkipBack, SkipForward, Settings, Video } from 'lucide-react';
import { API_BASE_URL } from '../../api/config';

export default function EnterpriseVideoPlayer() {
  const { activeSessionId, currentVideoTime, setCurrentVideoTime, isPlaying, setIsPlaying, seekTo } = useTimeline();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [viewMode, setViewMode] = useState<'original' | 'annotated' | 'split'>('annotated');
  const [playbackRate, setPlaybackRate] = useState(1.0);

  // Sync state to video
  useEffect(() => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.play().catch(() => setIsPlaying(false));
      } else {
        videoRef.current.pause();
      }
    }
  }, [isPlaying]);

  // Sync seekTo from other components
  useEffect(() => {
    if (seekTo !== null && videoRef.current) {
      videoRef.current.currentTime = seekTo;
      setCurrentVideoTime(seekTo);
    }
  }, [seekTo]);

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentVideoTime(videoRef.current.currentTime);
    }
  };

  const togglePlay = () => setIsPlaying(!isPlaying);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const videoUrl = activeSessionId 
    ? (viewMode === 'original' 
      ? `${API_BASE_URL}/videos/${activeSessionId}/original` 
      : `${API_BASE_URL}/videos/${activeSessionId}/annotated`)
    : '';

  return (
    <div className="flex flex-col h-full bg-slate-900 text-white relative">
      {/* Video Header / View Switcher */}
      <div className="absolute top-0 left-0 right-0 p-4 bg-gradient-to-b from-black/80 to-transparent flex justify-between items-start z-10">
        <div className="flex gap-2">
          <div className="bg-black/50 backdrop-blur border border-white/20 rounded-lg p-1 flex">
            <button 
              className={`px-3 py-1 text-xs font-medium rounded ${viewMode === 'original' ? 'bg-primary-600' : 'hover:bg-white/10'}`}
              onClick={() => setViewMode('original')}
            >Original</button>
            <button 
              className={`px-3 py-1 text-xs font-medium rounded ${viewMode === 'annotated' ? 'bg-primary-600' : 'hover:bg-white/10'}`}
              onClick={() => setViewMode('annotated')}
            >Annotated</button>
            <button 
              className={`px-3 py-1 text-xs font-medium rounded ${viewMode === 'split' ? 'bg-primary-600' : 'hover:bg-white/10'}`}
              onClick={() => setViewMode('split')}
              disabled
              title="Split view in development"
            >Split View</button>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1.5 px-2 py-1 bg-green-500/20 text-green-400 border border-green-500/30 rounded text-xs font-bold">
            <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span> LIVE SYNC
          </span>
        </div>
      </div>

      {/* Video Container */}
      <div className="flex-1 relative bg-black flex items-center justify-center overflow-hidden group" onClick={togglePlay}>
        {!activeSessionId ? (
          <div className="flex flex-col items-center justify-center text-slate-500">
            <Video className="w-12 h-12 mb-2 opacity-50" />
            <p>Select or upload a video session to play</p>
          </div>
        ) : (
          <video
            ref={videoRef}
            src={videoUrl}
            className="w-full h-full object-contain"
            onTimeUpdate={handleTimeUpdate}
            onEnded={() => setIsPlaying(false)}
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            crossOrigin="anonymous"
          />
        )}
      </div>

      {/* Custom Controls */}
      <div className="bg-slate-900 border-t border-slate-800 p-3">
        {/* Progress Bar */}
        <div className="w-full h-1.5 bg-slate-700 rounded-full mb-3 cursor-pointer relative"
             onClick={(e) => {
               const rect = e.currentTarget.getBoundingClientRect();
               const pos = (e.clientX - rect.left) / rect.width;
               if (videoRef.current) {
                 videoRef.current.currentTime = pos * (videoRef.current.duration || 100);
               }
             }}>
          <div 
            className="absolute top-0 left-0 h-full bg-primary-500 rounded-full" 
            style={{ width: `${(currentVideoTime / (videoRef.current?.duration || 100)) * 100}%` }}
          />
        </div>
        
        {/* Buttons */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button onClick={togglePlay} className="hover:text-primary-400 transition-colors">
              {isPlaying ? <Pause className="w-6 h-6" /> : <Play className="w-6 h-6" />}
            </button>
            <div className="text-sm font-mono">
              {formatTime(currentVideoTime)} / {formatTime(videoRef.current?.duration || 0)}
            </div>
          </div>
          
          <div className="flex items-center gap-4 text-slate-400">
            <button className="hover:text-white transition-colors text-xs font-bold border border-slate-600 rounded px-1.5 py-0.5"
                    onClick={() => {
                      const newRate = playbackRate >= 2 ? 0.5 : playbackRate + 0.5;
                      setPlaybackRate(newRate);
                      if (videoRef.current) videoRef.current.playbackRate = newRate;
                    }}>
              {playbackRate}x
            </button>
            <button className="hover:text-white transition-colors"><Settings className="w-5 h-5" /></button>
            <button className="hover:text-white transition-colors"><Maximize className="w-5 h-5" /></button>
          </div>
        </div>
      </div>
    </div>
  );
}
