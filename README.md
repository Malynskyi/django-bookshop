# Book Store Project

![Django CI](https://github.com/Malynskyi/django-bookshop/actions/workflows/django.yml/badge.svg)

![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen)

Django-based book store application with REST API, JWT authentication, Redis caching, Celery tasks, Docker, NGINX, CI/CD and PostgreSQL.

---

## Multi-Service Architecture

This solution consists of two independent Django applications.

### Project A — Django Bookshop

Main e-commerce application providing:

- Books API
- Categories API
- Shopping Cart
- Orders
- JWT Authentication
- User Management

### Project B — Atlas Warehouse Service

Independent warehouse management service providing:

- Stock Management
- Warehouse Inventory API
- JWT Protected Endpoints
- Swagger Documentation

---

## Interservice Communication

Bookshop communicates with Atlas Warehouse Service through REST API using JWT authentication.

### Architecture Diagram

```text
┌──────────────────────────┐
│      Django Bookshop     │
│        Project A         │
└─────────────┬────────────┘
              │
              │ JWT + REST API
              ▼
┌──────────────────────────┐
│ Atlas Warehouse Service  │
│        Project B         │
└──────────────────────────┘
```

### Bookshop Endpoint

```text
/api/warehouse-status/
```

### Atlas Endpoint

```text
/api/stock/
```

### Example Response

```json
{
  "service": "bookshop",
  "atlas_status": "connected",
  "warehouses": []
}
```

---

## Features

- Django REST Framework API
- JWT Authentication
- Custom User Model
- Groups & Permissions
- Class-Based Views
- Redis Caching
- Celery Async Tasks
- Celery Beat Periodic Tasks
- PostgreSQL Database
- Docker & Docker Compose
- Gunicorn Production Server
- NGINX Reverse Proxy
- Swagger / OpenAPI Documentation
- Internationalization (EN / UA)
- Async Views
- Integration Tests
- API Tests
- Coverage ≥ 70%
- GitHub Actions CI/CD
- Multi-Service Architecture
- Interservice REST API Communication
- Error Handling & Logging

---

## Technologies

### Backend

- Django 5
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Celery Beat
- SimpleJWT

### DevOps

- Docker
- Docker Compose
- NGINX
- Gunicorn
- GitHub Actions
- Render Deployment
- Sentry Monitoring

### Testing

- Pytest
- Coverage
- Integration Tests
- API Tests

---

## Local Setup

Clone repository:

```bash
git clone https://github.com/Malynskyi/django-bookshop.git
cd django-bookshop
```

Run project:

```bash
docker compose up --build
```

Run migrations:

```bash
python manage.py migrate
```

Run tests:

```bash
pytest
```

---

## Live Services

### Django Bookshop

Application:

https://django-bookshop.onrender.com

Swagger Documentation:

https://django-bookshop.onrender.com/api/docs/

Warehouse Status Endpoint:

https://django-bookshop.onrender.com/api/warehouse-status/

---

### Atlas Warehouse Service

Application:

https://atlas-service-ovqp.onrender.com

Swagger Documentation:

https://atlas-service-ovqp.onrender.com/api/docs/

Health Check:

https://atlas-service-ovqp.onrender.com/health/

---

## Testing

Project includes:

- Unit Tests
- Integration Tests
- API Tests

Coverage:

```text
85%
```

Run coverage:

```bash
pytest --cov
```

---

## AI Usage

This project was improved with AI assistance.

AI was used for:

- Code review of complex Django views
- Test generation for models, forms, views and user flows
- Async views implementation
- Docstrings generation
- README improvement

All AI-generated suggestions were reviewed, tested and modified manually before being committed.