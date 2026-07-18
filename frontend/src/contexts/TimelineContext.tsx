import React, { createContext, useContext, useState, ReactNode } from 'react';

interface TimelineContextType {
  currentVideoTime: number;
  setCurrentVideoTime: (time: number) => void;
  isPlaying: boolean;
  setIsPlaying: (playing: boolean) => void;
  selectedCustomerId: number | null;
  setSelectedCustomerId: (id: number | null) => void;
  selectedZone: string | null;
  setSelectedZone: (zone: string | null) => void;
  selectedProductId: string | null;
  setSelectedProductId: (id: string | null) => void;
  seekTo: number | null;
  setSeekTo: (time: number | null) => void;
}

const TimelineContext = createContext<TimelineContextType | undefined>(undefined);

export function TimelineProvider({ children }: { children: ReactNode }) {
  const [currentVideoTime, setCurrentVideoTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedCustomerId, setSelectedCustomerId] = useState<number | null>(null);
  const [selectedZone, setSelectedZone] = useState<string | null>(null);
  const [selectedProductId, setSelectedProductId] = useState<string | null>(null);
  const [seekTo, setSeekTo] = useState<number | null>(null);

  return (
    <TimelineContext.Provider value={{
      currentVideoTime, setCurrentVideoTime,
      isPlaying, setIsPlaying,
      selectedCustomerId, setSelectedCustomerId,
      selectedZone, setSelectedZone,
      selectedProductId, setSelectedProductId,
      seekTo, setSeekTo
    }}>
      {children}
    </TimelineContext.Provider>
  );
}

export function useTimeline() {
  const context = useContext(TimelineContext);
  if (context === undefined) {
    throw new Error('useTimeline must be used within a TimelineProvider');
  }
  return context;
}
