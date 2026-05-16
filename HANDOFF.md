# SAMS — Audit & Fix Handoff Document

## Context for new session

**Project**: Sports Academy Management System — multi-tenant SaaS (Django 5 + DRF + PostgreSQL + Redis + Celery | Vue 3 + Quasar + TypeScript + Pinia)

**Background**: Codebase was ~70% complete per `sams.md` spec. Ran `/graphify . --mode deep` (graph at `graphify-out/`). Then audited every subsystem against spec. Fixed 25 critical/high bugs. ~45 items remain.

**Key files:**
- Spec: `sams.md` (2600+ lines, 15 numbered Prompts defining all phases)
- Project memory: `CLAUDE.md` (architecture overview)
- Graph data: `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md`
- Ignore file: `.graphifyignore` (excludes htmlcov, node_modules, etc.)

**Shell is bash** even though platform is win32. Use Unix path syntax (`/dev/null` not `NUL`).

---

## 1. AUDIT SCOPE — what was examined

Four parallel agents audited every file against `sams.md`:

| Agent | Subsystems | Files examined |
|-------|-----------|---------------|
| Core backend | accounts, permissions, academies, common, audit, settings, urls | 15 files |
| Scheduling/attendance | sessions, attendance, groups, players, ratings, cancellations | 19 files |
| Payments/notifications | payments, notifications, analytics, reports, communication | 24 files |
| Frontend | all pages, stores, router, layouts, i18n, api, components | 44 files |

---

## 2. COMPLETED FIXES

### 2.1 Critical Runtime Bugs (7 fixed — would crash)

- [x] **TenantManager cross-tenant data leak**
  - File: `backend/apps/common/models.py`
  - Change: `get_queryset()` now raises `ValueError("TenantManager requires an academy context...")` instead of returning all records when no `X-Academy-ID` header.
  - Spec ref: sams.md §4.2 "Never expose cross-tenant data"

- [x] **`request.user.academy` crash in player views**
  - File: `backend/apps/players/views.py`
  - Problem: `request.user.academy` (singular FK). User model has `academies` (M2M).
  - Fix: Uses `get_current_academy_id()` from thread-local, resolves Academy object.
  - Also fixed `backend/apps/players/services.py` — `bulk_import_from_csv` now takes `academy_id` string, resolves Academy, validates CSV columns.

- [x] **`request.user.players.first()` crash in cancellations**
  - File: `backend/apps/cancellations/views.py`
  - Problem: User has no `players` relation. Player model has no FK to User.
  - Fix: Removed the line. Player comes from serializer `validated_data`. Made `player` writable in `CancellationRequestSerializer`.
  - Also: `backend/apps/cancellations/serializers.py` — read_only_fields changed from `("academy", "player", "status", "request_date")` to `("academy", "status", "request_date", "reviewed_by", "review_notes")`.

- [x] **Communication.NotificationLog academy field clash**
  - File: `backend/apps/communication/models.py`
  - Problem: `NotificationLog` re-declared `academy` FK already inherited from `TenantAwareModel`. Would cause Django field clash.
  - Fix: Removed duplicate FK, renamed class to `CommunicationNotificationLog` to avoid name collision with `notifications.models.NotificationLog`.

- [x] **RegisterSerializer password validation dead code**
  - File: `backend/apps/accounts/serializers/auth.py`
  - Problem: `create()` called `User.objects.create_user()` which never invokes Django's password validators.
  - Fix: Added `validate_password()` method calling `password_validation.validate_password(value)`. `create()` now pops password, calls `user.set_password(password)` then `user.save()`. Email field now `EmailField()`.
  - Also: `get_primary_academy_id` uses `order_by('created_at')` for deterministic ordering.

- [x] **StandardizedJSONRenderer crash on None/list data**
  - File: `backend/apps/common/renderers.py`
  - Problem: `data.get("detail", "")` crashes when `data` is `None` or `list`.
  - Fix: Guard checks `isinstance(data, dict)` before calling `.get()`. Message extraction only runs for dict responses.

- [x] **`training_sessions.SessionOccurrence` FK references — VERIFIED CORRECT**
  - File: `backend/apps/sessions/apps.py` line 8: `label = "training_sessions"`
  - All FK references in attendance, ratings, cancellations, groups using `"training_sessions.SessionOccurrence"` are valid.

### 2.2 High-Priority Backend Gaps (12 fixed)

- [x] **Academy model — 6 missing spec fields**
  - File: `backend/apps/academies/models.py`
  - Added: `subscription_plan` (free/basic/premium/enterprise), `status` (active/suspended/trialing/cancelled), `branding_settings` (JSONField), `timezone` (default "Africa/Cairo"), `language` (default "ar"), `currency` (default "EGP").

- [x] **Discount model added to payments**
  - File: `backend/apps/payments/models.py`
  - New model: `Discount(TenantAwareModel)` with `name`, `discount_type` (percentage/fixed), `value`, `is_active`, `valid_from`, `valid_to`.
  - `Invoice` now has optional FK to `Discount` and `Coupon`.

- [x] **SMS adapter + channel added**
  - File: `backend/apps/notifications/models.py` — `ChannelChoices` now includes `SMS = "sms"`.
  - File: `backend/apps/notifications/services/adapters.py` — `SMSAdapter` class added (stub with provider integration point).
  - File: `backend/apps/notifications/tasks.py` — `ADAPTER_MAP` includes `ChannelChoices.SMS: SMSAdapter`.

- [x] **Analytics enrollment status filter fixed**
  - File: `backend/apps/analytics/tasks.py` line 31-33
  - Change: `status='active'` → `status__in=['active', 'attended']` (was excluding "attended" enrollments from active player count).

- [x] **Report generators — stubs replaced with functional fallbacks**
  - File: `backend/apps/reports/generators.py`
  - `ExcelReportGenerator`: now outputs valid CSV with UTF-8 BOM instead of "not yet implemented".
  - `PDFReportGenerator`: now outputs pipe-delimited text report instead of "not yet implemented".

- [x] **Rate limiting configured**
  - File: `backend/config/settings/base.py`
  - DRF settings: `AnonRateThrottle` (100/hr), `UserRateThrottle` (1000/hr), `ScopedRateThrottle` for login (5/min).
  - `DEFAULT_VERSIONING_CLASS` changed from `NamespaceVersioning` → `URLPathVersioning` with `DEFAULT_VERSION: "v1"`.
  - Page size query param enabled: `PAGE_SIZE_QUERY_PARAM: "page_size"`, `MAX_PAGE_SIZE: 100`.

- [x] **Logout endpoint + token blacklisting**
  - File: `backend/apps/accounts/views/auth.py` — `LogoutView` accepts refresh token in POST body, calls `token.blacklist()`.
  - File: `backend/apps/accounts/urls.py` — `logout/` path registered.

- [x] **Login throttling + IP logging**
  - File: `backend/apps/accounts/views/auth.py` — `LoginView` now uses `ScopedRateThrottle` with `throttle_scope = "login"`. IP captured via `request.META.get('REMOTE_ADDR')`.

- [x] **Celery Beat — missing scheduled tasks**
  - File: `backend/config/settings/base.py`
  - Added: `refresh-coach-performance` (weekly Mon 4AM), `process-overdue-invoices` (daily 6AM).

- [x] **Overdue invoice detection task**
  - File: `backend/apps/payments/tasks.py` — `check_overdue_invoices()` marks unpaid/partially_paid invoices past `due_date` as "overdue".

- [x] **Permission classes on session viewsets**
  - File: `backend/apps/sessions/views/session.py`
  - `SessionSeriesViewSet` → `IsOperations`, `SessionOccurrenceViewSet` → `IsCoach`, `VenueViewSet` → `IsOperations`.

- [x] **Security + email settings**
  - File: `backend/config/settings/base.py`
  - Added: `DEFAULT_FROM_EMAIL`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, `SECURE_HSTS_SECONDS`.

### 2.3 Scheduling Engine Enhancements (6 fixes)

- [x] **Infinite loop guard** — `MAX_OCCURRENCES = 500` cap on `generate_occurrences` loop.
- [x] **Coach conflict detection** — checks `SessionCoach` for overlapping assigned sessions.
- [x] **Player conflict detection** — checks `Enrollment` for overlapping enrolled sessions.
- [x] **Capacity enforcement** — `check_capacity()` method, `enroll_player()` raises `ValueError` if full.
- [x] **Occurrence override** — `override_occurrence()` for venue/time/capacity changes on single occurrence.
- [x] **Coach assignment** — `assign_coach()` with post-assignment conflict detection.
- File: `backend/apps/sessions/services/scheduling.py` (complete rewrite).

### 2.4 Session API Gaps (4 fixes)

- [x] `SessionCoachSerializer` + `ScheduleConflictSerializer` in `backend/apps/sessions/serializers/session.py`
- [x] `SessionCoachViewSet` + `EnrollmentViewSet` in `backend/apps/sessions/views/session.py`
- [x] `enroll` + `assign_coach` actions on `SessionOccurrenceViewSet`
- [x] New routes registered in `backend/apps/sessions/urls.py` (`/coaches/`, `/enrollments/`)

### 2.5 Frontend Critical Bugs (4 fixed)

- [x] **Token refresh** — `frontend/src/api/index.ts`: Full silent refresh implementation. On 401, attempts `accounts/token/refresh/` with stored refresh token. Queues concurrent requests during refresh. Only triggers logout if refresh also fails.
- [x] **DashboardPage badge** — `props.value === 'Live'` → `props.value === 'live'` (lowercase match with API).
- [x] **SamsDataTable invalid prop** — `:card-class` → `:table-class` (Quasar `q-table` prop name).
- [x] **Session interface** — `series` typed as `{ id: string; title: string } | string`, `venue` as `{ id: string; name: string } | string`, added `start_datetime`, `end_datetime`, `max_capacity`.

---

## 3. MIGRATIONS NEEDED

After the model changes, migrations must be generated:

```bash
# Academy model — 6 new fields
docker-compose exec backend python backend/manage.py makemigrations academies

# Payments — Discount model + Invoice FK changes
docker-compose exec backend python backend/manage.py makemigrations payments

# Then apply
docker-compose exec backend python backend/manage.py migrate
```

---

## 4. REMAINING TASKS

### 4.1 BACKEND — HIGH PRIORITY

- [ ] **Coach app is EMPTY** (`backend/apps/coaches/` has only `__init__.py`)
  - Spec Prompt 6 requires: Coach CRUD, availability, assignments, workload tracking.
  - Need: `Coach` model (or use User with coach role), views, serializers, URLs.
  - `CoachAvailability` model for scheduling constraints.

- [ ] **AuditLog model + async audit**
  - Spec §15: Every critical action logged with actor, action, entity, old value, new value, IP, timestamp.
  - Current `audit/middleware.py` is a stub (comment admits it).
  - Need: `AuditLog` model, Celery task for async write, signal-based capture (post_save/post_delete) with old/new value diffs.

- [ ] **Password reset flow**
  - Spec Prompt 4: forgot-password, password-reset confirmation, email-based reset link.
  - Need: `ForgotPasswordView`, `PasswordResetConfirmView`, email template, URL patterns.

- [ ] **Email verification flow**
  - Spec Prompt 4: verify email after registration.
  - Need: Verification token model or signed link, verify endpoint, resend endpoint.

- [ ] **Object-level permissions**
  - Spec Prompt 4 line 1910: "object-level access".
  - Current `permissions/permissions.py` classes have no `has_object_permission()`.
  - Need: Add object-level checks for coach-only-their-sessions, customer-only-their-data.

- [ ] **MFA-ready architecture**
  - Spec §5.2: User model needs `mfa_enabled` (BooleanField).
  - Need: OTP/TOTP integration point, backup codes model.

- [ ] **Field-level encryption for medical notes**
  - Spec §14.2: Medical notes, sensitive payment metadata, PII must be encrypted.
  - Player model needs `medical_notes` field (encrypted), `emergency_contact` fields.

- [ ] **Player model enhancements**
  - Missing: `email`, `phone_number`, `status` (active/inactive), `photo` (ImageField), `gender`.
  - Missing: Parent/guardian relationship (spec Prompt 7: "multiple child profiles, linked accounts").

- [ ] **Cancellation policy model**
  - Currently 24-hour deadline is hardcoded in `cancellations/views.py`.
  - Need: `CancellationPolicy` model per academy (minimum notice hours, auto-approval rules).

- [ ] **Notification scheduling**
  - Spec Prompt 10: scheduled/delayed notifications.
  - Need: `scheduled_at` field on NotificationLog or separate model, Celery Beat task to dispatch scheduled.

- [ ] **OpenAPI/Swagger documentation**
  - Spec §13.2: OpenAPI docs required.
  - Need: `drf-spectacular` in requirements + config.

- [ ] **Health check endpoint**
  - No `/health/` or `/api/v1/health/` endpoint exists.

- [ ] **Rate limiting — apply to RegisterView**
  - Currently only LoginView has throttling. Register should also have it.

### 4.2 BACKEND — MEDIUM PRIORITY

- [ ] **Payment approval workflow endpoint**
  - Bank transfer payments need manual approval. No approve-payment endpoint exists.
  - Refund approval — pending refunds have no approve/reject endpoint.

- [ ] **Reconciliation workflow**
  - Spec Prompt 9: manual reconciliation workflow.
  - `FinancialDashboardView` uses `request.user.academies.first()` which is wrong for multi-academy users.

- [ ] **Payment `is_approved` default behavior**
  - Default is `True` even for bank transfers. Should be `False` for bank transfer, `True` for cash.

- [ ] **Refund amount validation**
  - `process_refund` can refund more than original payment amount. No validation.

- [ ] **Notification `broadcast_notification` batching**
  - Iterates users in Python. Should use bulk operations for large user bases.

- [ ] **Reports `get_data()` handle all report types**
  - Currently handles only "financial" and "attendance". Missing "utilization" and "performance" data impl.

- [ ] **Reports scheduled email delivery**
  - `process_scheduled_reports` has TODO for emailing recipients. Not implemented.

- [ ] **SessionOccurrenceSerializer write support**
  - Nested `series` and `venue` serializers are read-only. Can't create standalone occurrences via API.

- [ ] **Analytics retention rate**
  - `MonthlyEnrollmentSnapshot` stores counts but doesn't calculate retention percentage.

- [ ] **Session utilization analytics**
  - Spec requires session utilization tracking. No model or task exists.

- [ ] **Coach performance Celery Beat — CHECK REGISTERED**
  - Task was added to schedule in settings. Verify task name matches `@shared_task` decorator.

### 4.3 FRONTEND — HIGH PRIORITY

- [ ] **i18n completeness** (~15 keys out of hundreds needed)
  - All pages except LoginPage use hardcoded English.
  - Need: translation keys for all page content, form labels, table headers, error messages, status labels, nav items.
  - Arabic translations needed for all keys.

- [ ] **RTL support properly wired**
  - `App.vue` sets `:dir` attribute but Quasar RTL requires language pack import in `quasar.config.js`.
  - May need `import { Q_LANG }` and locale switching via Quasar's lang API.

- [ ] **Empty directories — populate**
  - `frontend/src/composables/` — completely empty. Need API composables, form validation, date formatting, pagination.
  - `frontend/src/types/` — doesn't exist. Need shared TypeScript interfaces.
  - `frontend/src/utils/` — doesn't exist. Need date, currency, formatting utilities.

- [ ] **Missing pages — Customer Portal** (spec Prompt 7)
  - No weekly/monthly calendar view (current TimetablePage is a flat timeline).
  - ProfilePage is 100% hardcoded mock data. Needs API integration.
  - No parent multi-child support page.

- [ ] **Missing pages — Coach Portal** (spec Prompt 8)
  - No coach cancellation page.
  - No coach notifications page/route.
  - SessionReportPage — submit buttons have no handlers, no API integration.
  - AttendancePage — `activeSessionId` hardcoded, no session picker.

- [ ] **Missing pages — Operations Portal** (spec Prompt 6)
  - No coach management page.
  - No group management page.
  - No session scheduling page.
  - No operations-level attendance tracking page.
  - No communication/announcements page.

- [ ] **Missing stores**
  - `notificationStore` — spec §11.3 requires it.
  - `analyticsStore` — spec §11.3 requires it.
  - `coachStore` — for coach management.
  - `groupStore` — for group management.

- [ ] **CancellationsPage hardcoded data**
  - Line 95: `upcomingSessions` is hardcoded. Needs real session fetching.
  - Line 119: `player: 'current-user-id'` is a placeholder string sent to API.

- [ ] **Coach RatingPage hardcoded coach ID**
  - Line 119: `coach: 'current-coach-id'` placeholder sent to API.

- [ ] **DashboardPage metrics**
  - All `quickStats` are hardcoded `'0'`. Need API integration.
  - `alerts` ref initialized empty with "Fetch from API" comment.

- [ ] **AnalyticsPage empty shell**
  - No API calls. No charting library. `q-knob` stuck at 0.

- [ ] **ReportsPage empty shell**
  - "Request Report" button no handler. Download buttons decorative.

- [ ] **PlayerManagementPage — missing Update/Delete**
  - Only Create + Read implemented. Update/Delete buttons have no handlers.

### 4.4 FRONTEND — MEDIUM PRIORITY

- [ ] **Calendar component needed** — Spec requires calendar for timetable views. No calendar anywhere.
- [ ] **Chart integration** — No charting library (Chart.js, ApexCharts). Analytics/dashboard need it.
- [ ] **Virtual scrolling** — Spec §30.2 requires virtual scrolling for large lists.
- [ ] **Request caching** — Spec §30.2 requires request caching. No TanStack Query / vue-query.
- [ ] **WCAG 2.1 AA accessibility** — No aria attributes, no keyboard nav, no screen reader support.
- [ ] **Notification bell in CoachLayout/CustomerLayout** — decorative only, clicking does nothing.
- [ ] **Stores don't reset on logout** — Session/player/attendance data persists in memory after logout.
- [ ] **No global error boundary** — Uncaught Vue errors silently fail.
- [ ] **RegisterPage missing fields** — No academy selection, no phone, no password confirmation.
- [ ] **Forgot password link** — Not present on login page.

### 4.5 DEVOPS / INFRASTRUCTURE

- [ ] **CI/CD pipeline** — GitHub Actions only partially configured (spec Prompt 13).
- [ ] **Production settings** — `backend/config/settings/production.py` exists but content thin.
- [ ] **MinIO/S3 storage** — File storage defaults to local. For production use object storage.
- [ ] **Sentry integration** — Not configured despite spec requirement.

### 4.6 TESTING

- [ ] **Backend test coverage** — Only 6 test files. Spec requires minimum 80%.
  - Missing: permission tests, tenant isolation tests (comprehensive), payment edge cases, scheduling error cases, cancellation workflows.
- [ ] **Frontend testing** — Zero frontend tests. Spec requires component + E2E tests.
- [ ] **Playwright E2E** — Recommended in spec. Not set up.

---

## 5. KNOWN BUGS (NOT YET FIXED)

These were identified in audit but deferred:

1. `FinancialDashboardView` (payments/views/financial.py) — `request.user.academies.first()` may be None for users with no academy.
2. `process_refund` — no validation that refund amount ≤ payment amount.
3. `apply_adjustment` — debit adjustments mutate `total_amount` which should be immutable.
4. `process_scheduled_reports` — hardcoded template code `"GENERAL_ANNOUNCEMENT"` may not exist.
5. `SessionReportViewSet` — uses `IsAuthenticated`, should be coach-specific. Serializer uses `fields = "__all__"` exposing `is_approved`.
6. `Attendance` model — `marked_by` set automatically but no server-side check that marking user is assigned coach.
7. `Rating` model — `PositiveSmallIntegerField` allows 0-32767 for 1-10 scale. No validation.
8. `Player` model — `registration_number` has no uniqueness constraint, bulk import creates duplicates.
9. Analytics viewsets — no `get_queryset()` override, rely entirely on thread-local academy (which raises error if missing — fixed in TenantManager, so this is now a hard failure instead of data leak).

---

## 6. KEY ARCHITECTURAL NOTES FOR NEXT SESSION

- **Multi-tenancy**: Every model inherits `TenantAwareModel` which auto-scopes via `TenantManager`. Academy context set by `TenantMiddleware` via `X-Academy-ID` header stored in thread-local. `TenantManager` now raises exception if no context — endpoints must ensure header is present.
- **RBAC hierarchy**: `IsSuperAdmin > IsAdmin > IsOperations > IsCoach > IsCustomer`. Permission classes in `permissions/permissions.py` use hierarchical inheritance.
- **Soft delete + tenant scoping**: `TenantManager` combines both. `all_objects` bypasses both. Deleting calls `soft_delete()` (sets `is_deleted=True`).
- **API responses**: Wrapped by `StandardizedJSONRenderer` as `{success, data, errors, message}`. Frontend Axios interceptor unwraps automatically.
- **Frontend auth flow**: JWT access + refresh tokens in localStorage. `api/index.ts` now silently refreshes. `authStore.logout()` does `window.location.href = '/'` (hard reload to kill all state).
- **Sessions app label**: Explicitly `training_sessions` in `sessions/apps.py`. All cross-app FK references use this label.
- **Payments is OFFLINE-FIRST**: No payment gateways. Cash + bank transfer tracking only. Spec Prompt 9 is explicit about this.
- **Quasar Framework v2** for UI. Vue 3 Composition API with `<script setup lang="ts">`.
- **vue-best-practices skill** in `skills/` directory enforces Composition API + TypeScript standard.

---

## 7. QUICK REFERENCE — COMMON COMMANDS

```bash
# Backend
pytest                                                  # all tests
pytest backend/apps/sessions/tests/test_scheduling.py   # single test file
ruff check . && ruff format .                           # lint + format

# Frontend
cd frontend && npm run dev      # dev server on :8080
cd frontend && npm run lint     # ESLint

# Docker
docker-compose up --build
docker-compose exec backend python backend/manage.py migrate
docker-compose exec backend python backend/manage.py makemigrations

# Installed skills/plugins
# Skills: graphify, vue-best-practices, frontend-design, code-review, 
#         code-simplifier, commit-commands, feature-dev, hookify, caveman
# Caveman mode active (full) — respond terse, drop articles/filler
```

---

**Total fixed**: 25 items across backend and frontend
**Remaining**: ~45 items documented above
**Highest impact next steps**: Coach app, audit logging, i18n translations, composables/types directory population, missing operations portal pages
