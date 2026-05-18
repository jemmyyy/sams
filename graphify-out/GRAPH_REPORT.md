# Graph Report - .  (2026-05-15)

## Corpus Check
- Corpus is ~28,650 words - fits in a single context window. You may not need a graph.

## Summary
- 714 nodes · 1227 edges · 133 communities (101 shown, 32 thin omitted)
- Extraction: 60% EXTRACTED · 40% INFERRED · 0% AMBIGUOUS · INFERRED: 495 edges (avg confidence: 0.53)
- Token cost: 30,000 input · 15,343 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Attendance Tracking|Attendance Tracking]]
- [[_COMMUNITY_Django App Registry|Django App Registry]]
- [[_COMMUNITY_Django App Registry|Django App Registry]]
- [[_COMMUNITY_Frontend Dependencies|Frontend Dependencies]]
- [[_COMMUNITY_Django App Registry|Django App Registry]]
- [[_COMMUNITY_Django App Registry|Django App Registry]]
- [[_COMMUNITY_Core Identity & Tenants|Core Identity & Tenants]]
- [[_COMMUNITY_API Client Layer|API Client Layer]]
- [[_COMMUNITY_Authorization & Ratings|Authorization & Ratings]]
- [[_COMMUNITY_Analytics Scheduler|Analytics Scheduler]]
- [[_COMMUNITY_Report Generation|Report Generation]]
- [[_COMMUNITY_Audit & Notifications|Audit & Notifications]]
- [[_COMMUNITY_Authentication API|Authentication API]]
- [[_COMMUNITY_Payment Processing|Payment Processing]]
- [[_COMMUNITY_Group Management|Group Management]]
- [[_COMMUNITY_Notification Adapters|Notification Adapters]]
- [[_COMMUNITY_Cancellation System|Cancellation System]]
- [[_COMMUNITY_Communication Hub|Communication Hub]]
- [[_COMMUNITY_Internationalization (i18n)|Internationalization (i18n)]]
- [[_COMMUNITY_Vue Frontend Components|Vue Frontend Components]]
- [[_COMMUNITY_Frontend Tooling Config|Frontend Tooling Config]]
- [[_COMMUNITY_Payment Processing|Payment Processing]]
- [[_COMMUNITY_Module 22|Module 22]]
- [[_COMMUNITY_API Response Layer|API Response Layer]]
- [[_COMMUNITY_Frontend Tooling Config|Frontend Tooling Config]]
- [[_COMMUNITY_Security Policies|Security Policies]]
- [[_COMMUNITY_Module 27|Module 27]]
- [[_COMMUNITY_Django Configuration|Django Configuration]]
- [[_COMMUNITY_Vue Frontend Components|Vue Frontend Components]]
- [[_COMMUNITY_Module 30|Module 30]]
- [[_COMMUNITY_Vue Frontend Components|Vue Frontend Components]]
- [[_COMMUNITY_Module 32|Module 32]]
- [[_COMMUNITY_Database Migrations|Database Migrations]]
- [[_COMMUNITY_Database Migrations|Database Migrations]]
- [[_COMMUNITY_Report Generation|Report Generation]]
- [[_COMMUNITY_Module 36|Module 36]]
- [[_COMMUNITY_Module 38|Module 38]]
- [[_COMMUNITY_Django Configuration|Django Configuration]]
- [[_COMMUNITY_Module 43|Module 43]]
- [[_COMMUNITY_Frontend Tooling Config|Frontend Tooling Config]]
- [[_COMMUNITY_Module 46|Module 46]]
- [[_COMMUNITY_Audit & Notifications|Audit & Notifications]]
- [[_COMMUNITY_Audit & Notifications|Audit & Notifications]]
- [[_COMMUNITY_Audit & Notifications|Audit & Notifications]]
- [[_COMMUNITY_Module 84|Module 84]]
- [[_COMMUNITY_Module 85|Module 85]]
- [[_COMMUNITY_Module 86|Module 86]]
- [[_COMMUNITY_Module 87|Module 87]]
- [[_COMMUNITY_Module 88|Module 88]]
- [[_COMMUNITY_Module 89|Module 89]]
- [[_COMMUNITY_Player Management|Player Management]]
- [[_COMMUNITY_Player Management|Player Management]]
- [[_COMMUNITY_Session Scheduling|Session Scheduling]]
- [[_COMMUNITY_Session Scheduling|Session Scheduling]]

## God Nodes (most connected - your core abstractions)
1. `TenantAwareModel` - 45 edges
2. `CLAUDE.md Development Guide` - 24 edges
3. `Payment` - 22 edges
4. `Command` - 21 edges
5. `SessionOccurrence` - 20 edges
6. `GEMINI.md Project Mandates` - 20 edges
7. `UUIDModel` - 19 edges
8. `TimeStampedModel` - 19 edges
9. `NotificationLog` - 18 edges
10. `Invoice` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Offline Reconciliation Workflow` --semantically_similar_to--> `Audit Logging`  [INFERRED] [semantically similar]
  backend/apps/payments/README.md → CLAUDE.md
- `Shared-Schema Multi-Tenancy` --semantically_similar_to--> `Domain-Driven Modular Architecture`  [INFERRED] [semantically similar]
  CLAUDE.md → GEMINI.md
- `Vue 3 Frontend` --calls--> `Pinia State Management`  [INFERRED]
  frontend/index.html → GEMINI.md
- `Meta` --uses--> `TenantAwareModel`  [INFERRED]
  backend/apps/attendance/models.py → backend/apps/common/models.py
- `Meta` --uses--> `TenantAwareModel`  [INFERRED]
  backend/apps/groups/models.py → backend/apps/common/models.py

## Hyperedges (group relationships)
- **Financial Transaction Workflow** — invoice_model, payment_installment, financial_adjustment, refund_model, financial_integrity [EXTRACTED 1.00]
- **API Request Processing Pipeline** — django_backend, drf_api, jwt_auth, shared_schema_multitenancy, standardized_responses, audit_logging [INFERRED 0.85]
- **Docker Service Stack** — postgresql_db, redis_cache, django_backend, celery_task_queue, celery_beat, nginx_proxy, vue3_frontend [EXTRACTED 1.00]

## Communities (133 total, 32 thin omitted)

### Community 0 - "Attendance Tracking"
Cohesion: 0.06
Nodes (31): Attendance, Meta, AttendanceSerializer, Meta, AttendanceViewSet, BaseCommand, Command, Command (+23 more)

### Community 1 - "Django App Registry"
Cohesion: 0.09
Nodes (56): Academies App, Accounts App, Analytics App, Attendance App, Audit App, Audit Logging, Axios HTTP Client, Celery Beat Scheduler (+48 more)

### Community 2 - "Django App Registry"
Cohesion: 0.1
Nodes (26): AbstractUser, Academy, User, NotificationLogAdmin, NotificationTemplateAdmin, UserNotificationPreferenceAdmin, ChannelChoices, NotificationLog (+18 more)

### Community 3 - "Frontend Dependencies"
Cohesion: 0.05
Nodes (42): author, dependencies, axios, pinia, quasar, @quasar/extras, vue, vue-i18n (+34 more)

### Community 4 - "Django App Registry"
Cohesion: 0.14
Nodes (25): Coupon, FinancialAdjustment, Invoice, Meta, Payment, PaymentInstallment, Refund, export_financial_report() (+17 more)

### Community 5 - "Django App Registry"
Cohesion: 0.08
Nodes (10): TenantMiddleware, clear_current_academy_id(), set_current_academy_id(), Player, Meta, PlayerSerializer, PlayerService, PlayerViewSet (+2 more)

### Community 6 - "Core Identity & Tenants"
Cohesion: 0.2
Nodes (26): Meta, CoachPerformanceSnapshot, DailyAttendanceSnapshot, DailyRevenueSnapshot, Meta, MonthlyEnrollmentSnapshot, CoachPerformanceSnapshotSerializer, DailyAttendanceSnapshotSerializer (+18 more)

### Community 7 - "API Client Layer"
Cohesion: 0.06
Nodes (25): academyId, api, authStore, isLoginRequest, token, accessGranted, authStore, requiredRole (+17 more)

### Community 8 - "Authorization & Ratings"
Cohesion: 0.13
Nodes (14): Command, Role, UserRole, IsAdmin, IsCoach, IsCustomer, IsOperations, IsSuperAdmin (+6 more)

### Community 9 - "Analytics Scheduler"
Cohesion: 0.11
Nodes (15): refresh_daily_revenue(), refresh_monthly_enrollment(), delete(), get(), _make_key(), Utility for academy-scoped caching., set(), TenantSafeCache (+7 more)

### Community 10 - "Report Generation"
Cohesion: 0.23
Nodes (10): GeneratedReport, ScheduledReport, SessionReport, GeneratedReportSerializer, Meta, ScheduledReportSerializer, SessionReportSerializer, GeneratedReportViewSet (+2 more)

### Community 11 - "Audit & Notifications"
Cohesion: 0.12
Nodes (8): AuditMiddleware, SoftDeleteManager, TenantManager, get_current_academy_id(), broadcast_notification(), _check_throttle(), send_notification(), template()

### Community 12 - "Authentication API"
Cohesion: 0.2
Nodes (9): APIView, LoginSerializer, Meta, RegisterSerializer, UserSerializer, test_send_notification_success(), LoginView, ProfileView (+1 more)

### Community 14 - "Group Management"
Cohesion: 0.3
Nodes (7): Group, GroupCoach, Meta, GroupCoachSerializer, GroupSerializer, Meta, GroupViewSet

### Community 15 - "Notification Adapters"
Cohesion: 0.24
Nodes (6): ABC, BaseChannelAdapter, EmailAdapter, InAppAdapter, PushAdapter, WhatsAppAdapter

### Community 16 - "Cancellation System"
Cohesion: 0.31
Nodes (4): CancellationRequest, CancellationRequestSerializer, Meta, CancellationRequestViewSet

### Community 17 - "Communication Hub"
Cohesion: 0.31
Nodes (4): Announcement, AnnouncementSerializer, Meta, AnnouncementViewSet

### Community 18 - "Internationalization (i18n)"
Cohesion: 0.2
Nodes (6): DefineDateTimeFormat, DefineLocaleMessage, DefineNumberFormat, i18n, MessageLanguages, MessageSchema

### Community 19 - "Vue Frontend Components"
Cohesion: 0.32
Nodes (5): clickCount, props, todoCount, Meta, Todo

### Community 20 - "Frontend Tooling Config"
Cohesion: 0.25
Nodes (7): editor.bracketPairColorization.enabled, editor.codeActionsOnSave, editor.defaultFormatter, editor.formatOnSave, editor.guides.bracketPairs, eslint.validate, typescript.tsdk

### Community 22 - "Module 22"
Cohesion: 0.4
Nodes (3): AppConfig, NotificationsConfig, SessionsConfig

### Community 24 - "Frontend Tooling Config"
Cohesion: 0.5
Nodes (3): printWidth, $schema, singleQuote

## Knowledge Gaps
- **123 isolated node(s):** `allow`, `Run administrative tasks.`, `Migration`, `Meta`, `Utility for academy-scoped caching.` (+118 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TenantAwareModel` connect `Core Identity & Tenants` to `Attendance Tracking`, `Django App Registry`, `Django App Registry`, `Django App Registry`, `Authorization & Ratings`, `Report Generation`, `Group Management`, `Cancellation System`, `Communication Hub`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `TestNotificationService` connect `Django App Registry` to `Audit & Notifications`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `Academy` connect `Django App Registry` to `Attendance Tracking`, `Authorization & Ratings`, `Django App Registry`, `Core Identity & Tenants`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 40 inferred relationships involving `TenantAwareModel` (e.g. with `DailyRevenueSnapshot` and `Meta`) actually correct?**
  _`TenantAwareModel` has 40 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `Payment` (e.g. with `Command` and `Command`) actually correct?**
  _`Payment` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Command` (e.g. with `Academy` and `Role`) actually correct?**
  _`Command` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `allow`, `Run administrative tasks.`, `Migration` to the rest of the system?**
  _123 weakly-connected nodes found - possible documentation gaps or missing edges._