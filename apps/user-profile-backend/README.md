# Mini Project: User Profile Management API (Backend)

Stack: Django REST Framework + SimpleJWT

## Quickstart (local)
1. Create Virtual Environment and Install Dependencies
   ```bash
   python -m venv venv
   venv\Scripts\activate   # or source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt   # Optional: For local development/testing
   ```
2. Prepare Environment Variables
   ```bash
   cp .env.example .env
   # Modify DJANGO_SECRET_KEY / DB configuration, etc., in .env as needed
   ```
3. Initialize Database and Create Superuser (using default SQLite)
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Start the Server
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
5. Run Tests
   ```bash
   python manage.py test users
   ```

## Required / Common Environment Variables
Sourced from .env (See .env.example for template):
- `DJANGO_SECRET_KEY` (Required; must be customized for production)

- `DJANGO_DEBUG` (Default is False; should be False in production)

- `DJANGO_ALLOWED_HOSTS` (Comma-separated list; avoid using *)

- `DJANGO_CORS_ALLOWED_ORIGINS` (Comma-separated list of frontend domains/ports)

- `Database (Optional, defaults to SQLite if left empty)`: `DJANGO_DB_ENGINE`, `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, `DJANGO_DB_HOST`, `DJANGO_DB_PORT`

-Security: `DJANGO_SECURE_HSTS_SECONDS `(Recommended >0 for production)
## API Overview
- Authentication: `POST /api/auth/login/` to get `access/refresh` tokens; `POST /api/auth/refresh/` to refresh the access token.

-Profile: `GET /api/user/profile/` (View currently logged-in user profile); `PATCH /api/user/profile/`(Update editable fields).

## Design Highlights
- JWT Authentication: The profile endpoints are protected by the IsAuthenticated permission.

- Security Configuration: `CORS`, `ALLOWED_HOSTS`, and security headers are sourced from environment variables. Default settings are geared towards local development; explicit configuration is required for production.
