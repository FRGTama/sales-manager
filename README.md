# Sharework Sales Management System

A demo sales management system with a hierarchical model: **Sale → Agency → Track Record**. Built with FastAPI (async), React, SQLite, and TanStack Query.

## Architecture

```
sharework-sales/
├── backend/               # FastAPI async API
│   └── app/
│       ├── models.py      # SQLAlchemy ORM entities
│       ├── schemas.py     # Pydantic request/response schemas
│       ├── repositories.py# Data access layer (abstract + SQL impl)
│       ├── services.py    # Business logic layer (abstract + impl)
│       ├── database.py    # Async engine + session factory
│       ├── routes/        # FastAPI controllers (sales, agencies, track_records, stats)
│       └── main.py        # App factory + DI wiring
├── frontend/              # React (Vite) + Tailwind + TanStack Query
│   └── src/
│       ├── api/           # Axios client + query hooks
│       ├── components/    # Layout, DataTable, Modal, StatCard, StatusChart, Forms
│       └── pages/         # Dashboard, Sales, Agencies, TrackRecords
└── package.json           # Root scripts (concurrently)
```

### SOLID Principles Applied

- **Single Responsibility** — models, schemas, repositories, services, routes each have one concern
- **Open/Closed** — new entities or stats queries extend without modifying existing code
- **Liskov Substitution** — service/repository ABCs define interfaces; implementations are swappable
- **Interface Segregation** — separate Pydantic schemas per operation; focused repository interfaces
- **Dependency Inversion** — services depend on abstract repository interfaces; FastAPI DI wires concretions

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

- Python 3.10+
- Node.js 18+

### Setup

```bash
# Install backend dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# Install root dev dependency
npm install
```

### Run (both servers)

```bash
npm run dev
```

- Backend: http://localhost:8000 (API docs: http://localhost:8000/docs)
- Frontend: http://localhost:5173

### Run separately

```bash
# Backend only
npm run dev:backend

# Frontend only
npm run dev:frontend
```

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

## What's Done / Not Done

**Done:**
- Full main flow: Create Sale → Agency → Track Record → Dashboard
- Async SQLite database with SQLAlchemy
- RESTful API with FastAPI
- Clean layered architecture (repositories → services → routes)
- TanStack Query for automatic cache invalidation
- Recharts pie chart for status breakdown
- Tailwind CSS styling

**Not Done (explicitly out of scope):**
- Update/delete operations
- Authentication / authorization
- Pagination
- Search / filtering
- Data export
- Deployment
