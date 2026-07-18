# API Integration
## Configuration
Base URL: `http://localhost:8000`
Middleware: CORSMiddleware enabled on FastAPI backend.

## Endpoints Consumed
- `GET /advisor/summary`: Fetches daily KPI rollups and critical alerts.
- `GET /advisor/store-health`: Fetches AI computed store health score.
- `GET /advisor/recommendations`: Fetches heuristic rule-based recommendations.
# Component Catalog
## KPICard
- Purpose: Display top-level business metrics.
- Props: title, value, trend, icon, subtitle, status
- Locations: ExecutiveDashboard, CustomerAnalytics, BusinessAnalytics

## SystemStatus
- Purpose: Render live connection status to backend engines.
- Props: None
- Locations: ExecutiveDashboard, StoreLayout
# Dashboard Design System
## Typography
- Font Family: Inter / System Sans
- Sizes: base (14px), lg (16px), xl (20px), 2xl (24px)

## Colors
- Primary: #22c55e (Green for Retail Vision AI branding)
- Background: #f8fafc (Light) / #0f172a (Dark)
- Surface/Card: #ffffff (Light) / #1e293b (Dark)
- Status: Red (Critical), Amber (Warning), Green (Good)

## Layout Grid
- Max Width: 7xl (1280px)
- Gap: 6 (24px) spacing for main widgets
# Final Phase 5 Executive Summary
Phase 5 (Enterprise Dashboard) is complete.

## Accomplishments
- **Landing Page**: Created a highly polished SaaS landing page.
- **Auth Flow**: Built an enterprise login portal with Role Selection.
- **Enterprise Shell**: Built a robust navigation sidebar with dark/light theming support.
- **AI Executive Dashboard**: Fully visualized the Store Health and Business metrics.
- **Interactive Store Layout**: Created a live store layout mapping zone performance.
- **Analytics Views**: Shipped Behavior, Customer, and Business data visualization tabs.

## Status
- UI Completeness: PASS
- Backend Integration: PASS
- SaaS Aesthetics: PASS

Phase 5 is APPROVED.
# Frontend Architecture
## Stack
- Framework: React 18 + Vite
- Language: TypeScript
- Routing: React Router v6
- Styling: Tailwind CSS
- Data Viz: Recharts
- Icons: Lucide React

## Folder Structure
```
frontend/
  src/
    api/         # API configuration and fetchers
    components/  # Reusable UI components
    layouts/     # Page layouts (MainLayout)
    pages/       # View components (Dashboard, Analytics)
    lib/         # Utility functions (clsx, twMerge)
```
