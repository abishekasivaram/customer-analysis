import React, { useState } from 'react';
import { Download, FileJson, FileText, Table, Check } from 'lucide-react';

interface ReportItem {
  name: string;
  type: string;
  size: string;
  date: string;
  url: string;
  filename: string;
}

export default function ReportCenter() {
  const [downloading, setDownloading] = useState<string | null>(null);

  const reports: ReportItem[] = [
    { 
      name: 'Executive Summary', 
      type: 'PDF', 
      size: '2.8 KB', 
      date: 'Today, 09:00 AM',
      url: '/api/outputs/reports/executive_summary.pdf',
      filename: 'executive_summary.pdf'
    },
    { 
      name: 'Business Metrics', 
      type: 'PDF', 
      size: '2.6 KB', 
      date: 'Today, 09:00 AM',
      url: '/api/outputs/reports/business_metrics.pdf',
      filename: 'business_metrics.pdf'
    },
    { 
      name: 'Store Health Report', 
      type: 'PDF', 
      size: '2.2 KB', 
      date: 'Today, 09:00 AM',
      url: '/api/outputs/reports/store_health_report.pdf',
      filename: 'store_health_report.pdf'
    },
    { 
      name: 'Advisor Recommendations', 
      type: 'PDF', 
      size: '2.2 KB', 
      date: 'Yesterday, 18:00 PM',
      url: '/api/outputs/reports/advisor_recommendations.pdf',
      filename: 'advisor_recommendations.pdf'
    },
  ];

  const handleDownload = async (report: ReportItem) => {
    setDownloading(report.name);
    try {
      const response = await fetch(report.url);
      if (!response.ok) {
        throw new Error(`Failed to fetch report: ${response.status}`);
      }
      const blob = await response.blob();
      const objectUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = objectUrl;
      link.download = report.filename;
      document.body.appendChild(link);
      link.click();
      window.URL.revokeObjectURL(objectUrl);
      document.body.removeChild(link);
    } catch (error) {
      console.warn("Direct fetch download failed, triggering fallback:", error);
      const link = document.createElement('a');
      link.href = report.url;
      link.download = report.filename;
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } finally {
      setTimeout(() => setDownloading(null), 1000);
    }
  };

  const getIcon = (type: string) => {
    switch (type) {
      case 'PDF': return <FileText className="w-5 h-5 text-rose-500" />;
      case 'JSON': return <FileJson className="w-5 h-5 text-yellow-500" />;
      case 'CSV': return <Table className="w-5 h-5 text-green-500" />;
      case 'Markdown': return <FileText className="w-5 h-5 text-blue-500" />;
      default: return <FileText className="w-5 h-5 text-rose-500" />;
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
                    <button 
                      onClick={() => handleDownload(r)}
                      disabled={downloading === r.name}
                      className="p-2 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-950/30 rounded-lg transition-colors inline-flex items-center gap-2 text-sm font-medium cursor-pointer disabled:opacity-50"
                      title={`Download ${r.filename}`}
                    >
                      {downloading === r.name ? (
                        <>
                          <Check className="w-4 h-4 text-green-500" /> Downloading...
                        </>
                      ) : (
                        <>
                          <Download className="w-4 h-4" /> Download PDF
                        </>
                      )}
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
