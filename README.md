# Darukaa.Earth

Darukaa.Earth is a production-oriented geospatial carbon and biodiversity intelligence platform built for environmental project monitoring, map-based site management, analytics, ML-powered anomaly detection, AI summarization, and operational reporting.

## Problem statement

Environmental programs need a way to manage project sites, monitor carbon and biodiversity outcomes, detect anomalies, and generate shareable insights across teams. Existing workflows are often fragmented across spreadsheets, maps, and disconnected dashboards.

## Solution

Darukaa.Earth consolidates project data, geospatial site records, environmental uploads, analytics, AI insights, and reporting into one modular full-stack platform with a React frontend and Python FastAPI backend.

## Key features

- Project and site management
- Mapbox GIS integration with polygon editing
- Environmental dataset upload and validation
- Carbon and biodiversity analytics
- ML-based anomaly and prediction workflows
- AI insight summaries and natural-language assistant
- Alerts, notifications, reports, and audit tracking
- JWT authentication and RBAC

## Architecture

- Frontend: React, Vite, TypeScript, Tailwind-ready CSS
- Backend: FastAPI, SQLAlchemy, PostgreSQL + PostGIS
- Data science: pandas, NumPy, scikit-learn
- GIS: Mapbox GL JS, Mapbox Draw, GeoAlchemy2
- Deployability: Docker, Docker Compose, GitHub Actions

## Technology stack

- React + Vite + TypeScript
- Python + FastAPI
- PostgreSQL + PostGIS
- SQLAlchemy + Alembic
- Mapbox GL JS + Mapbox Draw
- Chart.js/Recharts
- JWT + bcrypt + RBAC
- pytest + Ruff + Black

## Local setup

1. Clone the repository.
2. Copy `.env.example` to `.env` and fill in values.
3. Start Postgres/PostGIS using Docker Compose. The backend applies Alembic migrations before serving.
4. Start the backend locally with `alembic upgrade head`, then run the API.
5. Start the frontend.

## Environment variables

See `.env.example` for required values.

## Docker setup

```bash
docker compose up --build
```

## Database migration

```bash
cd backend
alembic upgrade head
```

The local SQLite test path continues to bootstrap tables automatically and applies the legacy `sites.geometry` column repair when needed. Production and Compose deployments should use Alembic as the schema authority.

## Demo data setup

```bash
cd backend
python scripts/seed_demo_data.py
```

## Testing

```bash
cd backend
pytest
cd frontend
npm run lint
npm run build
```

## Deployment

The project is structured to support Vercel frontend deployment and Render or Railway-compatible backend deployment.

## CI/CD

GitHub Actions workflows for linting, testing, and deployment-ready validation should be added in later phases.

## Security

- JWT authentication with secure secret configuration
- Password hashing with bcrypt
- Input validation and ORM-based queries
- CORS and environment-based configuration
- Protected APIs and role checks

## ML methodology

The ML layer is designed around actual stored environmental data with model metadata, evaluation metrics, and explainability summaries.

## AI methodology

AI-powered insights are generated from structured backend analytics data with safe fallbacks when external APIs are unavailable.

## GIS methodology

Map and geometry processing are designed around PostGIS-enabled geospatial operations and GeoJSON export/import workflows.

## Limitations

- Real satellite or AI provider configuration requires valid API keys.
- Some advanced GIS and ML features are architecture-ready and require dataset coverage.

## Future enhancements

- Real-time sensor ingestion
- Satellite imagery integration
- Computer vision workflows
- Expanded dashboard automation

## Screenshots

Screenshots will be added as the application matures.

## Demo credentials

Demo credentials are generated at runtime or seeded during setup for testing. The exact values are configured in the seed script and environment files.

## Repository status

This repository is currently in Phase 1 setup state and is ready for the next implementation phase.
