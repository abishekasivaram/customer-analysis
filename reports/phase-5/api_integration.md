# API Integration
## Configuration
Base URL: `http://localhost:8000`
Middleware: CORSMiddleware enabled on FastAPI backend.

## Endpoints Consumed
- `GET /advisor/summary`: Fetches daily KPI rollups and critical alerts.
- `GET /advisor/store-health`: Fetches AI computed store health score.
- `GET /advisor/recommendations`: Fetches heuristic rule-based recommendations.
