# user-profile-frontend

Vue 2 + Element UI app for user profile management.

## Setup
- From repo root, install once: `npm install`
- Env (create `.env` in this folder if needed):
  - `VUE_APP_API_BASE_URL` (prod/base URL, default `http://localhost:8000`)
  - `VUE_APP_API_PROXY_TARGET` (dev proxy target for `/api`, default `http://localhost:8000`)

## Scripts
- `npm run dev` (from repo root) or `npm run dev --workspace user-profile-frontend`
- `npm run build`
- `npm run lint`
- `npm test` (placeholder; returns 0)

Dev server proxies `/api` to `VUE_APP_API_PROXY_TARGET` to avoid CORS during local development.
