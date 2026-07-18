import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import ExecutiveDashboard from './pages/ExecutiveDashboard';
import Login from './pages/Login';
import LandingPage from './pages/LandingPage';
import StoreLayout from './pages/StoreLayout';
import AIAdvisorDashboard from './pages/AIAdvisorDashboard';
import CustomerAnalytics from './pages/CustomerAnalytics';
import BehaviorAnalytics from './pages/BehaviorAnalytics';
import BusinessAnalytics from './pages/BusinessAnalytics';
import ReportCenter from './pages/ReportCenter';
import VideoWorkspace from './pages/VideoWorkspace';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<ExecutiveDashboard />} />
          <Route path="/advisor" element={<AIAdvisorDashboard />} />
          <Route path="/layout" element={<StoreLayout />} />
          <Route path="/customer" element={<CustomerAnalytics />} />
          <Route path="/behavior" element={<BehaviorAnalytics />} />
          <Route path="/business" element={<BusinessAnalytics />} />
          <Route path="/reports" element={<ReportCenter />} />
          <Route path="/workspace" element={<VideoWorkspace />} />
        </Route>
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
