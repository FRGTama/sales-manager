# Sharework Sales Management

Live demo: https://sharework.tama-dev.org/

The goal is to show the main sales-management flow working end-to-end, not to build a full CRM. The app lets a user create Sales, assign Agencies to Sales, create Track Records for Agencies, and view basic dashboard statistics.

## Tech Stack

- Backend: FastAPI, async SQLAlchemy, Pydantic, asyncpg
- Frontend: React, Vite, Tailwind CSS, TanStack Query, Axios, Recharts
- Database: PostgreSQL
- Local runner: root `npm run dev` starts backend and frontend together

## Main Flow

```text
Create Sale -> Create Agency assigned to Sale -> Create Track Record assigned to Agency -> View Dashboard
```

Data relationships:

- One Sale can manage many Agencies.
- One Agency belongs to one Sale.
- One Agency can have many Track Records.
- One Track Record belongs to one Agency.

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── repositories.py    # Database access layer
│   │   ├── services.py        # Business logic layer
│   │   ├── database.py        # Async database setup
│   │   ├── main.py            # FastAPI app setup
│   │   └── routes/            # API route modules
│   ├── tests/                 # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/               # Axios client and query hooks
│   │   ├── components/        # Shared UI components/forms
│   │   └── pages/             # Dashboard, Sales, Agencies, Track Records
│   └── package.json
├── docker-compose.yml
├── docker-compose.prod.yml
├── AI_USAGE.md
└── README.md
```

## Setup

### Prerequisites

- Python 3.13+
- Node.js 22+
- PostgreSQL database
- Docker, optional

### Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Fill in these values:

```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@YOUR_HOST:5432/postgres
TEST_DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@YOUR_HOST:5432/sharework_test
```

`DATABASE_URL` is used by the running app. `TEST_DATABASE_URL` is used by backend tests and should point to a separate disposable test database.

## Install Dependencies

Install root dev dependencies:

```bash
npm install
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

Or install everything with:

```bash
npm run install:all
```

## Run The Project

Start backend and frontend together:

```bash
npm run dev
```

Default URLs:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

Run backend only:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run frontend only:

```bash
cd frontend
npm run dev
```

The frontend uses the Vite dev proxy, so API calls to `/api` are forwarded to the backend during development.

## Run With Docker

```bash
docker compose up --build
```

This starts the app containers. A PostgreSQL connection still needs to be provided through the environment variables.

## Tests

Run backend tests:

```bash
cd backend
pytest
```

Run frontend tests:

```bash
cd frontend
npm test
```

Run frontend lint:

```bash
cd frontend
npm run lint
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/sales` | List Sales |
| `POST` | `/api/sales` | Create Sale |
| `GET` | `/api/sales/{id}` | Get Sale with Agencies |
| `PUT` | `/api/sales/{id}` | Update Sale |
| `DELETE` | `/api/sales/{id}` | Delete Sale |
| `GET` | `/api/agencies` | List Agencies |
| `POST` | `/api/agencies` | Create Agency assigned to Sale |
| `GET` | `/api/agencies/{id}` | Get Agency with Track Records |
| `PUT` | `/api/agencies/{id}` | Update Agency |
| `DELETE` | `/api/agencies/{id}` | Delete Agency |
| `GET` | `/api/track-records` | List Track Records |
| `POST` | `/api/track-records` | Create Track Record assigned to Agency |
| `PUT` | `/api/track-records/{id}` | Update Track Record |
| `DELETE` | `/api/track-records/{id}` | Delete Track Record |
| `GET` | `/api/stats` | Dashboard statistics |

## Completed

- Sale list and create flow.
- Agency list and create flow with Sale assignment.
- Track Record list and create flow with Agency assignment.
- Dashboard showing:
  - active Sales count
  - total Agencies
  - total Track Records
  - Track Records grouped by status
- Backend relationship validation:
  - Agency creation checks that the Sale exists.
  - Track Record creation checks that the Agency exists.
- Update and delete flows for Sales, Agencies, and Track Records.
- Frontend forms, modals, tables, and dashboard chart.
- Backend tests for the main API behavior.
- Frontend component/page tests.
- `AI_USAGE.md` describing how AI was used during development.
- Live deployment

## Not Completed / Out Of Scope

- Login, authentication, and role-based permissions.
- Load balancing.
- Advanced statistics for the dashboard
- Full production CRM workflow.
- Advanced filtering, search, and pagination.
- File upload/export features.
- Audit logs or activity history.


