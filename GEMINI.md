# SAMS (Sports Academy Management System) - Project Mandates

## Core Objectives
Building a production-grade multi-tenant SaaS platform for sports academies in Egypt.
- Multi-tenancy
- High concurrency
- Financial workflows
- Scheduling
- Notifications
- Analytics
- Mobile-first operation
- Arabic and English support
- Enterprise security standards

## 1. Backend Stack
- Python 3.12+
- Django 5+
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- JWT authentication
- Dockerized infrastructure

## 2. Frontend Stack
- Vue 3
- Quasar Framework
- TypeScript
- Pinia
- Axios

## 3. Architecture Rules
- Multi-tenant SaaS from day one.
- Every operational entity must belong to an academy tenant.
- Never expose cross-tenant data.
- Use UUID primary keys.
- Use soft deletes where applicable.
- Use asynchronous processing for notifications and heavy tasks.
- Never tightly couple business domains.
- Maintain modular domain-driven app architecture.
- Build mobile-first responsive UI.
- Support Arabic RTL and English LTR.

## 4. Security Rules
- RBAC enforced on backend.
- JWT token rotation.
- HTTPS-only architecture.
- Audit logging required.
- MFA-ready architecture.
- Financial records must never be hard deleted.

## 5. Scalability Rules
- Horizontally scalable backend.
- Queue-based architecture for background jobs.
- Redis caching support.
- Optimized PostgreSQL indexing.
- Async notifications and report generation.

## 6. Code Quality Rules
- Clean architecture.
- Type-safe frontend.
- Service-layer business logic.
- Repository/query abstraction when necessary.
- Comprehensive tests.
- No duplicated logic.
- Proper serializer validation.
- Reusable frontend composables/components.

## 7. Development Rules
- Generate production-ready code only.
- Never generate placeholder architecture.
- Never skip validation.
- Never skip permissions.
- Never trust frontend permissions.
- Never use synchronous heavy processing.
