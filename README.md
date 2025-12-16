# Integra Mini Project Monorepo

Monorepo for the Django REST backend and Vue 2 frontend, managed with npm workspaces and Turborepo.

## Layout
- `apps/user-profile-backend`: Django REST API (see its README for setup).
- `apps/user-profile-frontend`: Vue 2 + Element UI frontend.
- `packages/shared-types`: Shared TypeScript contracts (not yet consumed in apps; keep for future wiring).

## Prereqs
- Python 3.11+ with `venv`
- Node.js (npm) for frontend and turbo tooling

## Install
From repo root:
```bash
npm install
```
This installs turbo and workspace dependencies (frontend + shared types).

## Run
- Backend: `cd apps/user-profile-backend` and follow its `README.md` (`cp .env.example .env`, pip install, migrate, `python manage.py runserver`).
- Frontend dev: `npm run dev` (runs turbo -> `vue-cli-service serve` in `apps/user-profile-frontend`). You can scope: `npm run dev -- --filter user-profile-frontend`.
- Lint frontend: `npm run lint`
- Tests: placeholder only (no tests defined yet).

## Environment variables
- Backend: see `apps/user-profile-backend/.env.example`.
- Frontend:
  - `VUE_APP_API_BASE_URL` (prod/base URL, default `http://localhost:8000`)
  - `VUE_APP_API_PROXY_TARGET` (dev proxy target, default `http://localhost:8000`)

## House rules
- Keep secrets out of git (`.env`, database files, API keys).
- Run lint/tests per app before pushing.
