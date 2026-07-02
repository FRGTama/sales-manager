# Sharework Sales Management System

A demo sales management system with a hierarchical model: **Sale → Agency → Track Record**. Built with FastAPI (async), React, PostgreSQL, and TanStack Query.

## Architecture

```
sharework-sales/
├── backend/                # FastAPI async API
│   └── app/
│       ├── models.py       # SQLAlchemy ORM entities
│       ├── schemas.py      # Pydantic request/response schemas
│       ├── repositories.py # Data access layer
│       ├── services.py     # Business logic layer
│       ├── database.py     # Async engine + session factory
│       ├── routes/         # FastAPI controllers
│       └── main.py         # App factory + DI wiring
├── frontend/               # React (Vite) + Tailwind + TanStack Query
│   └── src/
│       ├── api/            # Axios client + query hooks
│       ├── components/     # Layout, DataTable, Modal, StatCard, StatusChart, Forms
│       └── pages/          # Dashboard, Sales, Agencies, TrackRecords
├── docker-compose.yml      # Backend + frontend (no local PG)
└── .env.example            # Required env vars template
```

## Features

| Feature | Description |
|---|---|
| **Sales** | List, create (name, phone, email, status) |
| **Agencies** | List, create (assigned to a Sale via dropdown) |
| **Track Records** | List, create (customer, revenue, status, notes, assigned to Agency) |
| **Dashboard** | Active sales count, total agencies, track records, status breakdown (PieChart) |

### Main Flow

`Create Sale → Create Agency (assign to Sale) → Create Track Record (assign to Agency) → View Dashboard`

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 22+
- Docker (optional, for Docker Compose)
- A PostgreSQL instance (e.g. [Supabase](https://supabase.com))

### Environment Variables

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

**Required vars:**

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | Production/development PostgreSQL connection | `postgresql+asyncpg://postgres:PW@db.abc.supabase.co:5432/postgres` |
| `TEST_DATABASE_URL` | Test database (separate DB on the same cluster) | `postgresql+asyncpg://postgres:PW@db.abc.supabase.co:5432/sharework_test` |

### Run with Docker Compose

```bash
docker compose up --build
```

- Backend: http://localhost:8000 (API docs: http://localhost:8000/docs)
- Frontend: http://localhost:5173

### Run locally (without Docker)

```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install root dev dependency
npm install

# Start both servers
npm run dev
```

> **Note:** The `DATABASE_URL` env var must be set in your shell or `.env` file when running without Docker.

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/sales` | List all sales |
| POST | `/api/sales` | Create a sale |
| GET | `/api/sales/{id}` | Get sale with agencies |
| GET | `/api/agencies` | List all agencies (with sale name) |
| POST | `/api/agencies` | Create agency (requires sale_id) |
| GET | `/api/agencies/{id}` | Get agency with track records |
| GET | `/api/track-records` | List all track records (with agency name) |
| POST | `/api/track-records` | Create track record (requires agency_id) |
| GET | `/api/stats` | Dashboard aggregations |
