# Integra Mini Project Monorepo

This repo will house the backend (Django REST) and the incoming frontend under a single workspace.

## Layout
- `apps/user-profile-backend`: Django REST API for user profiles (see its README for details).
- `apps/<frontend>`: placeholder for the frontend code once it is moved in.
- `packages/`: shared libraries or configs (empty for now).
  - `packages/shared-types`: shared TypeScript types for the API contracts (e.g., `UserProfile`, `UserProfileUpdatePayload`).

## Local setup
1) Clone and install tools
   - Python 3.11+ with `venv`
   - Node.js (for the future frontend and turborepo tooling)

2) Backend quickstart  
   `cd apps/user-profile-backend` and follow its `README.md` (`.env.example`, `pip install -r requirements*.txt`, `python manage.py migrate`, `python manage.py runserver`).

3) Frontend (coming soon)  
   When the frontend lands in `apps/<frontend>`, add its install/run scripts (e.g., `npm install`, `npm run dev`).

## Turbo repo intent
`turbo.json` is scaffolded for shared tasks (`lint`, `test`, `dev`) across apps. Add per-app commands in each package’s `package.json` and wire them to the pipeline when the frontend arrives.

## Environment variables
- Backend variables live in `apps/user-profile-backend/.env.example`.
- Consider adding root-level `.env.example` entries that are shared by both apps (e.g., API base URLs) once the frontend is in place.

## House rules
- Keep secrets out of git (`.env`, database files, API keys).
- Run lint/tests per app before pushing.
