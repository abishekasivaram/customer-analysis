import React from 'react';
import { cn } from '../lib/utils';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface KPICardProps {
  title: string;
  value: string | number;
  trend?: number;
  icon?: React.ReactNode;
  subtitle?: string;
  status?: 'good' | 'warning' | 'critical' | 'neutral';
}

export default function KPICard({ title, value, trend, icon, subtitle, status = 'neutral' }: KPICardProps) {
  const isPositive = trend !== undefined && trend > 0;
  const isNegative = trend !== undefined && trend < 0;

  const statusColors = {
    good: 'border-l-4 border-l-green-500',
    warning: 'border-l-4 border-l-yellow-500',
    critical: 'border-l-4 border-l-red-500',
    neutral: 'border-l-4 border-l-slate-300 dark:border-l-slate-700',
  };

  return (
    <div className={cn('card relative overflow-hidden flex flex-col justify-between group hover:shadow-md', statusColors[status])}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-sm font-medium text-slate-500 dark:text-dark-muted">{title}</h3>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
              {value}
            </span>
            {trend !== undefined && (
              <span className={cn(
                "flex items-center text-sm font-medium",
                isPositive ? "text-green-600 dark:text-green-400" : isNegative ? "text-red-600 dark:text-red-400" : "text-slate-500"
              )}>
                {isPositive ? <TrendingUp className="w-4 h-4 mr-1" /> : isNegative ? <TrendingDown className="w-4 h-4 mr-1" /> : <Minus className="w-4 h-4 mr-1" />}
                {Math.abs(trend)}%
              </span>
            )}
          </div>
        </div>
        {icon && (
          <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg text-primary-600 dark:text-primary-400">
            {icon}
          </div>
        )}
      </div>
      {subtitle && (
        <p className="text-xs text-slate-400 dark:text-slate-500">{subtitle}</p>
      )}
    </div>
  );
}
