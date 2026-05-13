# SAMS - Sports Academy Management System

Production-grade multi-tenant SaaS platform for sports academies.

## Architecture
- **Backend**: Django 5, DRF, PostgreSQL, Redis, Celery, Celery Beat.
- **Frontend**: Vue 3, Quasar Framework (to be implemented).
- **Infrastructure**: Dockerized with NGINX reverse proxy.

## Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local development)

## Getting Started

1. **Initialize Environment**:
   ```bash
   cp .env.template .env
   ```

2. **Build and Run Services**:
   ```bash
   docker-compose up --build
   ```

3. **Run Migrations**:
   ```bash
   docker-compose exec backend python backend/manage.py migrate
   ```

4. **Create Superuser**:
   ```bash
   docker-compose exec backend python backend/manage.py createsuperuser
   ```

## Development Commands

- **Run Tests**: `pytest`
- **Linting**: `ruff check .`
- **Formatting**: `ruff format .`
- **Celery Logs**: `docker-compose logs celery_worker`

## Multi-Tenancy
This project uses a shared-schema multi-tenancy approach. Every request must include the `X-Academy-ID` header to scope the data to the correct tenant.

## Standardized Responses
All API responses follow this format:
```json
{
    "success": true,
    "data": { ... },
    "errors": null,
    "message": ""
}
```
