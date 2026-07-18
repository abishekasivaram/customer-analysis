import React from 'react';
import { Download, FileJson, FileText, Table } from 'lucide-react';

export default function ReportCenter() {
  const reports = [
    { name: 'Executive Summary', type: 'JSON', size: '12 KB', date: 'Today, 09:00 AM' },
    { name: 'Business Metrics', type: 'CSV', size: '45 KB', date: 'Today, 09:00 AM' },
    { name: 'Store Health Report', type: 'Markdown', size: '5 KB', date: 'Today, 09:00 AM' },
    { name: 'Advisor Recommendations', type: 'JSON', size: '8 KB', date: 'Yesterday, 18:00 PM' },
  ];

  const getIcon = (type: string) => {
    switch (type) {
      case 'JSON': return <FileJson className="w-5 h-5 text-yellow-500" />;
      case 'CSV': return <Table className="w-5 h-5 text-green-500" />;
      case 'Markdown': return <FileText className="w-5 h-5 text-blue-500" />;
      default: return <FileText className="w-5 h-5 text-slate-500" />;
    }
  };

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Report Center</h1>
        <p className="text-slate-500 dark:text-slate-400">Download business analytics and AI advisor reports</p>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800">
                <th className="py-3 px-4 text-sm font-medium text-slate-500">Report Name</th>
                <th className="py-3 px-4 text-sm font-medium text-slate-500">Format</th>
                <th className="py-3 px-4 text-sm font-medium text-slate-500">Size</th>
                <th className="py-3 px-4 text-sm font-medium text-slate-500">Generated At</th>
                <th className="py-3 px-4 text-sm font-medium text-slate-500 text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((r, i) => (
                <tr key={i} className="border-b border-slate-100 dark:border-slate-800/50 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                  <td className="py-3 px-4 text-sm font-medium text-slate-900 dark:text-white flex items-center gap-2">
                    {getIcon(r.type)} {r.name}
                  </td>
                  <td className="py-3 px-4 text-sm text-slate-600 dark:text-slate-400">
                    <span className="px-2 py-1 bg-slate-100 dark:bg-slate-800 rounded text-xs font-medium">{r.type}</span>
                  </td>
                  <td className="py-3 px-4 text-sm text-slate-600 dark:text-slate-400">{r.size}</td>
                  <td className="py-3 px-4 text-sm text-slate-600 dark:text-slate-400">{r.date}</td>
                  <td className="py-3 px-4 text-right">
                    <button className="p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors inline-flex items-center gap-2 text-sm font-medium">
                      <Download className="w-4 h-4" /> Download
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
