# SAMS — Handoff Document (Updated 2026-05-16)

**Project**: Sports Academy Management System — Django 5 + DRF + PostgreSQL + Redis + Celery | Vue 3 + Quasar + TypeScript + Pinia

**State**: ~95% complete. All 40 tests pass. 15 commits from 3 audit passes.

---

## Quick Reference

```bash
# Backend
docker-compose exec backend python backend/manage.py migrate
docker-compose exec backend python -m pytest              # 40 tests, all pass
docker-compose exec backend python backend/manage.py shell_plus

# Frontend
cd frontend && npm run dev      # :8080
cd frontend && npm run lint     # ESLint

# Docker
docker-compose up --build
```

**Key files**: `sams.md` (spec), `CLAUDE.md` (architecture), `HANDOFF.md` (this file)

**Shell**: bash on Windows. Use Unix path syntax.

---

## Architecture Notes

- **Multi-tenancy**: `TenantAwareModel` base. `TenantManager` scopes by thread-local academy ID. Returns `qs.none()` when no context (safe for management commands). `all_objects` bypasses scoping. `TenantMiddleware` sets context from `X-Academy-ID` header.
- **RBAC**: `IsSuperAdmin > IsAdmin > IsOperations > IsCoach > IsCustomer`. Hierarchical — higher roles include lower ones. `has_object_permission()` on all classes.
- **Soft delete**: `TenantManager` filters `is_deleted=False`. `delete()` soft-deletes. `hard_delete()` for real delete.
- **API responses**: `{success, data, errors, message}` via `StandardizedJSONRenderer`. Frontend Axios interceptor unwraps.
- **Auth**: JWT access + refresh tokens. Silent refresh on 401. `authStore.logout()` hard-reloads to `/`.
- **Sessions app**: Label `training_sessions` in `apps.py`. All cross-app FKs use this label.
- **Payments**: Offline-first — cash + bank transfer tracking, no gateways.

---

## Completed (3 audit passes, ~90 items)

### Backend — New Apps & Major Features
- [x] Coach app: `Coach`, `CoachAvailability` models, CRUD viewsets, workload tracking, admin
- [x] Audit logging: `AuditLog` model, Celery async write, signal-based model change capture, middleware
- [x] CancellationPolicy: per-academy policy with auto-approval logic (9 tests)
- [x] Notification scheduling: `scheduled_at` field, Celery Beat dispatch every 5 min (5 tests)
- [x] Payment approval workflow: approve/reject for payments and refunds, auto-approve cash (6 tests)
- [x] Reconciliation: `reconciled` fields on Payment, reconcile endpoint, dashboard report

### Backend — Auth & Security
- [x] Password reset: `ForgotPasswordView`, `PasswordResetConfirmView`
- [x] Email verification: `VerifyEmailView`, `ResendVerificationView`
- [x] MFA-ready: `mfa_enabled`, `email_verified` on User
- [x] Rate limiting: AnonRateThrottle, UserRateThrottle, login throttling, RegisterView throttling
- [x] Object-level permissions: `has_object_permission()` on all role classes
- [x] Security settings: SSL redirect, HSTS, cookie security, secure proxy header
- [x] Sentry SDK configured in production settings

### Backend — Models Enhanced
- [x] Academy: subscription_plan, status, branding_settings, timezone, language, currency
- [x] Player: email, phone, status, photo, gender, medical_notes, emergency_contact, parent FK
- [x] Player: unique_together on (academy, registration_number)
- [x] Rating: MinValueValidator(1)/MaxValueValidator(10) on all score fields
- [x] User: mfa_enabled, email_verified
- [x] Payments: Discount, Coupon models
- [x] NotificationLog: scheduled_at field
- [x] Payment: reconciled, reconciled_at, reconciled_by

### Backend — Analytics
- [x] MonthlyEnrollmentSnapshot: retention_rate calculation
- [x] SessionUtilizationSnapshot: model, task, viewset
- [x] Celery Beat tasks: refresh-coach-performance, process-overdue-invoices, dispatch-scheduled-notifications, refresh-session-utilization

### Backend — Bug Fixes
- [x] TenantManager: returns `qs.none()` instead of raising (management command compat)
- [x] `request.user.academy` → `get_current_academy_id()` in player views
- [x] `request.user.players.first()` crash in cancellations
- [x] Communication.NotificationLog academy field clash
- [x] RegisterSerializer: password validation, password_confirm check
- [x] StandardizedJSONRenderer: guards for None/list data
- [x] SMS adapter + channel
- [x] Analytics enrollment status filter
- [x] Report generators: functional fallbacks
- [x] Logout: token blacklisting
- [x] Login: throttling + IP logging
- [x] Scheduling engine: infinite loop guard, conflict detection, capacity enforcement, overrides, coach assignment
- [x] Session viewsets: permission classes, nested routes
- [x] FinancialDashboardView: uses `get_current_academy_id()` instead of `user.academies.first()`
- [x] process_refund: validates refund amount ≤ payment amount
- [x] apply_adjustment: no longer mutates total_amount
- [x] SessionReportViewSet: IsCoach permission, explicit serializer fields
- [x] Report serializers: removed is_approved exposure

### Backend — Infrastructure
- [x] Health check: `/api/v1/health/`
- [x] Swagger/OpenAPI: `drf-spectacular` at `/api/v1/docs/`
- [x] Production settings: SMTP email, DB pooling, HSTS, S3/MinIO storage, Sentry
- [x] Pillow, django-storages, boto3, sentry-sdk in requirements

### Frontend — Infrastructure
- [x] `types/index.ts`: 30+ TypeScript interfaces
- [x] Composables: `useApi`, `usePagination`, `useFormValidation`, `useDateFormat`, `useCalendar`, `useChart`
- [x] Utils: `currency.ts`, `status.ts`, `validation.ts`, `cache.ts`
- [x] Stores: `notifications.ts`, `analytics.ts`, `coaches.ts`, `groups.ts`
- [x] Players store: `updatePlayer`, `deletePlayer` actions
- [x] Error boundary: Vue errorHandler + unhandled rejection handler
- [x] RTL: Quasar language pack imports (ar/en-US)
- [x] Request cache: in-memory TTL cache utility
- [x] Chart.js + vue-chartjs with dark theme composable
- [x] Calendar: `SamsCalendar` component + `useCalendar` composable
- [x] i18n: 70+ keys per locale (en-US, ar-EG) — validation, status, nav, session, player, payment, notification

### Frontend — Pages
- [x] Operations: CoachManagementPage, GroupManagementPage, SessionSchedulingPage, AttendanceTrackingPage, CommunicationsPage
- [x] Coach: CancellationsPage, NotificationsPage
- [x] PlayerManagementPage: edit dialog, delete confirmation
- [x] LoginPage: forgot password link
- [x] CoachLayout, OperationsLayout: updated nav tabs
- [x] Router: all new routes registered
- [x] Hardcoded data removed: AttendancePage, CancellationsPage, RatingPage

### Frontend — Bug Fixes
- [x] Token refresh: silent refresh with queue
- [x] DashboardPage: lowercase status match
- [x] SamsDataTable: `:card-class` → `:table-class`
- [x] Session interface: proper nested types

### DevOps
- [x] GitHub Actions CI: backend tests + frontend lint/build
- [x] Production settings: complete

### Testing
- [x] 40 tests pass (0 failures)
- [x] Permission tests (6), cancellation policy tests (9), notification scheduling tests (5), payment approval tests (6)
- [x] All pre-existing test failures fixed (academy context via autouse fixtures)

---

## Remaining (~10 items)

### Backend (4)
- [ ] Notification broadcast batching — iterates users in Python, should use bulk_create
- [ ] Reports: `get_data()` handle all report types (utilization, performance)
- [ ] Reports: scheduled email delivery (TODO in `process_scheduled_reports`)
- [ ] Field-level encryption for medical notes (currently plain text)

### Frontend (6)
- [ ] Virtual scrolling for large lists (Quasar supports natively — needs `q-virtual-scroll` usage)
- [ ] WCAG 2.1 AA polish (Quasar handles most — audit focus indicators, color contrast)
- [ ] DashboardPage: `quickStats` still hardcoded — needs API integration
- [ ] AnalyticsPage: no chart usage — wire up Chart.js with analytics API data
- [ ] ReportsPage: "Request Report" button needs handler to POST to reports API
- [ ] Customer ProfilePage: hardcoded mock data — needs API integration

### Testing (3)
- [ ] Backend coverage to 80% — current at ~40 tests, need more for accounts, coaches, groups, attendance, reports
- [ ] Frontend component tests — zero currently
- [ ] Playwright E2E — not set up

---

## Known Issues (Not Blocking)

1. `NotificationService.broadcast_notification` — iterates users in Python, slow for large bases
2. `process_scheduled_reports` — has TODO for email delivery
3. `Attendance.marked_by` — no server-side check that marking user is assigned coach
4. `SessionReportViewSet` — `is_approved` removed from serializer, approve workflow handled by report model field

---

## Git Log (Recent)

```
3092925 feat: add chart.js, CI/CD pipeline, MinIO/S3 storage config
dee49c1 fix: resolve all pre-existing test failures (12 → 0)
f9abc18 feat: add Sentry SDK, i18n translations, calendar component
63d6a38 feat: add request cache utility
7f6ec57 feat: add permission tests, production settings, error boundary
187c9be fix: add global error boundary, wire Quasar RTL language pack imports
eccea24 feat: add payment reconciliation workflow
9aa8c63 feat: add analytics retention rate, session utilization, player uniqueness
8af9bef fix: remove hardcoded data, add edit/delete handlers, add forgot password link
3947521 feat: add payment/refund approval workflow with TDD
cf25f06 fix: clean up nested test directories
7150e3c feat: add notification scheduling with Celery Beat dispatch
233c67c feat: add drf-spectacular Swagger/OpenAPI docs
0721c9f feat: add CancellationPolicy model with auto-approval logic
e2c2cf7 feat: build coach app, audit logging, auth flows, player fields, frontend infrastructure
2c65929 fix: resolve UUID display issues
```

---

**Remaining effort estimate**: ~2-3 sessions for testing coverage, frontend polish, and E2E.
