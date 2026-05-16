# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Backend (Django)
```bash
# Run all tests (requires DJANGO_SETTINGS_MODULE=config.settings.local)
pytest

# Run a single test file
pytest backend/apps/sessions/tests/test_scheduling.py

# Run a single test function/class
pytest backend/apps/sessions/tests/test_scheduling.py::TestSchedulingEngine::test_generate_occurrences

# Lint
ruff check .

# Format
ruff format .

# Django management (inside Docker)
docker-compose exec backend python backend/manage.py migrate
docker-compose exec backend python backend/manage.py createsuperuser
docker-compose exec backend python backend/manage.py shell_plus
```

### Frontend (Vue 3 / Quasar)
```bash
cd frontend
npm run dev        # Start dev server on port 8080
npm run build      # Production build
npm run lint       # ESLint
npm run format     # Prettier
```

### Docker
```bash
docker-compose up --build   # Build and start all services
docker-compose logs celery_worker
```

## Architecture

### Multi-Tenancy
Shared-schema multi-tenancy. Every operational model inherits from `TenantAwareModel` (see `backend/apps/common/models.py:57`) which auto-scopes querysets to the current academy via `TenantManager`. The academy ID is set per-request by `TenantMiddleware` (`backend/apps/academies/middleware.py:6`) reading the `X-Academy-ID` header, and stored in thread-local storage (`backend/apps/common/thread_local.py`). Every API call must include `X-Academy-ID`.

### Base Model Hierarchy
All models use UUID primary keys (`UUIDModel`), timestamps (`TimeStampedModel`), and soft deletes (`SoftDeleteModel`). Tenant-aware models use `TenantAwareModel` which combines all three and adds an `academy` FK with automatic scoping. `delete()` performs a soft delete; `hard_delete()` physically removes. Use `all_objects` manager to include soft-deleted records.

### Standardized API Responses
All API responses are wrapped by `StandardizedJSONRenderer` (`backend/apps/common/renderers.py:4`):
```json
{"success": true, "data": {...}, "errors": null, "message": ""}
```
The frontend Axios interceptor (`frontend/src/api/index.ts:23`) unwraps this automatically, so Vue components receive the raw `data` payload.

### RBAC
Five roles: `super_admin`, `admin`, `operations`, `coach`, `customer`. Roles are scoped per-academy via `UserRole` (`backend/apps/permissions/models.py:29`). Permission classes in `backend/apps/permissions/permissions.py` use hierarchical inheritance (e.g., `IsCoach` also allows operations, admin, super_admin). The frontend auth store (`frontend/src/stores/auth.ts`) mirrors this hierarchy in the `hasRole` getter.

### Django Settings
Settings use `django-environ` with `.env` file. Three-tier: `base.py` (shared), `local.py` (dev), `production.py`. `DJANGO_SETTINGS_MODULE` defaults to `config.settings.local` in pytest. Ini and Celery. Database uses `ATOMIC_REQUESTS = True`.

### Celery Beat Schedule
Defined in `base.py` — daily revenue/attendance refresh, monthly enrollment refresh, hourly scheduled reports processing.

### Frontend Routing
Role-based portal routing in `frontend/src/router/routes.ts`. Each portal (customer/coach/operations) uses a dedicated layout with lazy-loaded pages. Auth guards check `meta.requiresAuth` and `meta.role`. Login routes use `meta.targetRole` to pre-configure role-specific login.

### i18n
Vue I18n with `en-US` and `ar-EG` locales (`frontend/src/i18n/index.ts`). The app supports Arabic RTL and English LTR.

### Key App Modules
| App | Purpose |
|-----|---------|
| `academies` | Tenant model + `TenantMiddleware` |
| `accounts` | Custom `User` model (UUID, multi-academy), JWT auth views |
| `permissions` | `Role`, `UserRole`, DRF permission classes |
| `sessions` | Session series, occurrences, scheduling engine, venues |
| `attendance` | Session attendance tracking |
| `groups` | Player groups/teams |
| `players` | Player profiles |
| `payments` | Financial records, payment processing |
| `notifications` | Multi-channel notifications (push, email, SMS) via Celery |
| `analytics` | Aggregated metrics refreshed via Celery Beat |
| `audit` | `AuditMiddleware` logging all authenticated requests |
| `common` | Base models, renderer, exception handler, thread-local, caching |

### Testing
Uses `pytest` with `pytest-django`. Tests use `@pytest.mark.django_db` for DB access. Test settings disable migrations (`--nomigrations`) for speed. Fixtures create academy and other required models directly. Test files live alongside their app in `tests/` directories.
