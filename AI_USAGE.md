# AI Usage Report

## 1. AI Tools Used

- **OpenCode** (Claude-based CLI agent) — primary tool for generating both backend and frontend code

## 2. Parts Handled by AI

- **Project scaffolding** — generating the complete directory structure, configuration files
- **Backend architecture design** — applying Repository and Service patterns, abstract base classes, dependency injection
- **ORM models & schemas** — SQLAlchemy entity definitions with relationships, Pydantic schemas with validation
- **FastAPI routes** — all CRUD endpoints for sales, agencies, track records, and stats
- **Frontend components** — Layout, DataTable, Modal, StatCard, StatusChart, and all form components
- **API integration** — TanStack Query hooks, axios client, cache invalidation logic
- **Documentation** — README.md structure and content

## 3. Most Effective Prompts

**Prompt 1: Backend architecture**
> "implement a clean architecture for FastAPI + SQLAlchemy async with repository pattern, service layer, and FastAPI DI. Follow SOLID principles. Entities: Sale, Agency, TrackRecord with 1-N relationships."

**Prompt 2: Frontend structure**
> "create React components for a sales management SPA: Layout with sidebar navigation, DataTable, Modal, StatCard, and StatusChart (Recharts pie). Pages: Dashboard, Sales, Agencies, TrackRecords. Use TanStack Query for data fetching."

## 4. Errors Encountered & Debugging

- **Imports mismatch** — Initially the AgencyForm component imported `useAgencies` instead of `useSales` for the sale dropdown. Fixed by correcting the import.
- **Missing dropdown fields** — The AgencyForm and TrackRecordForm were missing the sale/agency dropdown selectors. Had to manually add `<select>` elements and wire form submission with the correct IDs.
- **Vite project path issue** — `npm create vite` nested the project at a wrong path due to directory pre-existence. Fixed by cleaning up and moving files to the correct location.

## 5. Key Takeaway

AI was most effective for generating boilerplate (models, schemas, components) and enforcing architectural patterns (abstract base classes, consistent naming). The main human value came from verifying data flow correctness — ensuring foreign keys are properly wired, dropdowns reference the right query, and mutations invalidate the correct cache keys.
