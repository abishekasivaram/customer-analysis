import React from 'react';
import { Link } from 'react-router-dom';
import { Store, BarChart, Lightbulb, Activity, ArrowRight, Shield, Zap } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-dark-bg font-sans">
      {/* Navbar */}
      <nav className="container mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2 text-primary-600 font-bold text-xl">
          <Store className="w-6 h-6" /> RetailVision AI
        </div>
        <div className="hidden md:flex gap-6 text-slate-600 dark:text-slate-300 font-medium text-sm">
          <a href="#features" className="hover:text-primary-600">Features</a>
          <a href="#benefits" className="hover:text-primary-600">Business Impact</a>
          <a href="#technology" className="hover:text-primary-600">Technology</a>
        </div>
        <div className="flex gap-4">
          <Link to="/login" className="px-5 py-2 text-primary-600 font-medium hover:bg-primary-50 rounded-lg transition-colors">
            Sign In
          </Link>
          <Link to="/login" className="px-5 py-2 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors">
            Get Demo
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="container mx-auto px-6 pt-20 pb-32 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-50 dark:bg-primary-900/30 text-primary-600 text-sm font-medium mb-8">
          <Zap className="w-4 h-4" /> Retail Intelligence Reimagined
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold text-slate-900 dark:text-white tracking-tight mb-8">
          Enterprise Analytics for <br className="hidden md:block"/>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-primary-400">Physical Retail</span>
        </h1>
        <p className="text-lg md:text-xl text-slate-600 dark:text-slate-400 max-w-2xl mx-auto mb-12">
          Transform your security camera feeds into actionable business intelligence. 
          Analyze customer behavior, optimize store layouts, and generate AI-driven ROI insights automatically.
        </p>
        <div className="flex justify-center gap-4">
          <Link to="/login" className="btn-primary px-8 py-4 text-lg flex items-center gap-2">
            Start Free Trial <ArrowRight className="w-5 h-5" />
          </Link>
          <a href="#preview" className="px-8 py-4 bg-white dark:bg-dark-card border border-slate-200 dark:border-slate-800 rounded-lg text-slate-700 dark:text-slate-300 font-medium hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
            View Dashboard
          </a>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="bg-white dark:bg-dark-card py-24 border-y border-slate-200 dark:border-slate-800">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-4">Complete Operational Intelligence</h2>
            <p className="text-slate-500 dark:text-slate-400">Everything you need to run your retail spaces like a software company.</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<Activity />} 
              title="Behavior Recognition" 
              desc="Detect interactions, dwell times, and product engagement without relying on subjective staff feedback."
            />
            <FeatureCard 
              icon={<BarChart />} 
              title="Advanced Flow Analytics" 
              desc="Identify dead zones, optimize high-traffic aisles, and reduce checkout congestion in real-time."
            />
            <FeatureCard 
              icon={<Lightbulb />} 
              title="AI Business Advisor" 
              desc="Our proprietary heuristic engine translates raw data into prioritized, actionable business recommendations."
            />
          </div>
        </div>
      </section>
      
      {/* Footer */}
      <footer className="container mx-auto px-6 py-12 text-center text-sm text-slate-500">
        <div className="flex items-center justify-center gap-2 mb-4">
          <Shield className="w-5 h-5 text-slate-400" /> Enterprise Grade Security & Privacy
        </div>
        <p>&copy; 2026 RetailVision AI. All rights reserved. Version 1.0.0-rc</p>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, desc }: { icon: React.ReactNode, title: string, desc: string }) {
  return (
    <div className="p-8 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-700/50 hover:shadow-lg transition-all duration-300 group">
      <div className="w-12 h-12 bg-white dark:bg-slate-700 rounded-xl flex items-center justify-center text-primary-600 mb-6 shadow-sm group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-3">{title}</h3>
      <p className="text-slate-600 dark:text-slate-400 leading-relaxed">{desc}</p>
    </div>
  )
}
