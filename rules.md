# School ERP — Development Rules & Architecture Guide

Version: 1.0
Framework: Flask + SQLAlchemy + Flask-Migrate + Jinja2
Deployment: Render
Database: SQLite (current phase)
Architecture: Modular Flask
Frontend: Server-rendered Jinja2 now, React-compatible later
Migration Strategy: Alembic-only
Status: Active Development / ERP Restructuring Phase

---

# 1. CORE DEVELOPMENT PRINCIPLES

This ERP MUST follow:

- Modular Flask architecture
- Single responsibility principle
- Role-based access control (RBAC)
- Migration-safe schema evolution
- Service-oriented business logic
- Zero circular imports
- Consistent database relationships
- Reusable Jinja components
- Blueprint isolation
- Environment-driven configuration

This codebase is intended to evolve into a scalable School ERP.

No shortcuts that create future architectural debt are allowed.

---

# 2. ABSOLUTE RULES (NON-NEGOTIABLE)

## NEVER DO THESE

❌ Never use `db.create_all()` in production runtime

❌ Never write manual `ALTER TABLE` SQL inside application startup

❌ Never hardcode passwords, secret keys, or admin credentials

❌ Never create duplicate model classes

❌ Never put all routes in one file

❌ Never import routes inside models

❌ Never import models inside templates

❌ Never bypass Flask-Migrate/Alembic

❌ Never mix authentication logic inside dashboard/business routes

❌ Never directly access session data for authorization checks

❌ Never perform database schema changes without migrations

❌ Never write business logic directly inside templates

❌ Never use circular imports as "temporary fixes"

❌ Never create fake/in-memory users like `TEACHER_ID = -1`

❌ Never use global mutable variables for auth/session logic

❌ Never expose admin routes without decorators

❌ Never use GET requests for destructive actions

❌ Never trust client-side validation alone

---

# 3. REQUIRED STACK

Backend:
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- Werkzeug security
- Jinja2

Frontend:
- HTML5
- CSS3
- Vanilla JS
- AJAX/fetch (future-ready)
- Dashboard cards
- Reusable template components

Database:
- SQLite for current phase
- PostgreSQL compatibility must be maintained

Deployment:
- Render

---

# 4. PROJECT STRUCTURE (MANDATORY)

attendance-app/
│
├── app.py
├── config.py
├── database.py
├── extensions.py
├── requirements.txt
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── student.py
│   ├── teacher.py
│   ├── admin.py
│   ├── academic.py
│   ├── attendance.py
│   ├── marks.py
│   ├── homework.py
│   ├── notification.py
│   └── communication.py
│
├── routes/
│   ├── __init__.py
│   │
│   ├── auth/
│   ├── admin/
│   ├── teacher/
│   ├── student/
│   └── api/
│
├── services/
│   ├── auth_service.py
│   ├── attendance_service.py
│   ├── marks_service.py
│   ├── notification_service.py
│   └── analytics_service.py
│
├── utils/
│   ├── decorators.py
│   ├── helpers.py
│   ├── validators.py
│   └── seed.py
│
├── templates/
│   ├── base.html
│   ├── components/
│   ├── auth/
│   ├── admin/
│   ├── teacher/
│   └── student/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
│
└── migrations/

---

# 5. AUTHENTICATION RULES

## Single User Model

ALL authentication MUST use ONE `User` table.

Example roles:
- admin
- teacher
- student

The `User` model is the ONLY Flask-Login identity source.

---

## Password Policy

Passwords MUST use:
- `generate_password_hash`
- `check_password_hash`

Plaintext passwords are forbidden.

---

## Session Policy

Student session:
- 10 minutes

Teacher session:
- 1 hour

Admin session:
- 1 hour

---

## Teacher Registration Flow

Flow:

1. Teacher self-registers
2. Account remains inactive
3. Admin approves/rejects
4. Approved teacher gains dashboard access

Teachers MUST NOT gain dashboard access before approval.

---

## Login Protection

Already-authenticated users:
- MUST NOT access login pages again
- MUST be redirected to their dashboard

---

# 6. ROLE-BASED ACCESS CONTROL (RBAC)

Decorators required:

- `admin_required`
- `teacher_required`
- `student_required`

Every protected route MUST use decorators.

Never rely solely on:
```python
if current_user.role == ...
```
