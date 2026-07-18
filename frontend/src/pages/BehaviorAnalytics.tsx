import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Eye, Hand, ShoppingBag } from 'lucide-react';

export default function BehaviorAnalytics() {
  const behaviorData = [
    { name: 'Viewing', value: 450, color: '#3b82f6' },
    { name: 'Touching', value: 300, color: '#f59e0b' },
    { name: 'Picking & Keeping', value: 150, color: '#10b981' },
    { name: 'Picking & Returning', value: 80, color: '#ef4444' },
  ];

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Behavior Analytics</h1>
        <p className="text-slate-500 dark:text-slate-400">Customer interactions and engagement</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card h-96">
          <h3 className="font-semibold text-slate-800 dark:text-white mb-6">Interaction Distribution</h3>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={behaviorData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {behaviorData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
              <Legend verticalAlign="bottom" height={36}/>
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-6">
          <div className="card flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-100 text-blue-600 rounded-xl"><Eye className="w-6 h-6"/></div>
              <div>
                <h4 className="font-bold text-slate-900 dark:text-white">Product Views</h4>
                <p className="text-sm text-slate-500">450 interactions</p>
              </div>
            </div>
            <span className="text-blue-600 font-bold">+12%</span>
          </div>
          <div className="card flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-amber-100 text-amber-600 rounded-xl"><Hand className="w-6 h-6"/></div>
              <div>
                <h4 className="font-bold text-slate-900 dark:text-white">Physical Touches</h4>
                <p className="text-sm text-slate-500">300 interactions</p>
              </div>
            </div>
            <span className="text-amber-600 font-bold">+5%</span>
          </div>
          <div className="card flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 text-green-600 rounded-xl"><ShoppingBag className="w-6 h-6"/></div>
              <div>
                <h4 className="font-bold text-slate-900 dark:text-white">Conversions (Kept)</h4>
                <p className="text-sm text-slate-500">150 interactions</p>
              </div>
            </div>
            <span className="text-green-600 font-bold">+18%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
