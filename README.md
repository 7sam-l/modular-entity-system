# Modular Entity System

A **production-quality** Django REST Framework backend managing Vendors, Products, Courses, and Certifications with clean, modular architecture.

```
Vendor → Product → Course → Certification
```

---

## What Changed in v2 (Production Refactor)

| Area | Before | After |
|---|---|---|
| Settings | Single `settings.py` with hardcoded secret | Split `base` / `development` / `production` + `.env` via `django-environ` |
| Views | 120–180 lines of copy-pasted CRUD per app | `MasterEntityMixin` + `MappingEntityMixin` — each view is ~40 lines |
| Serializers | Full validation duplicated in all 4 master apps | `BaseMasterSerializer` + `BaseMappingSerializer` — each serializer is 5 lines |
| Swagger schemas | Copy-pasted `openapi.Schema` blocks in every views.py | Single `core/swagger.py` with factory functions |
| Exception handling | No custom handler — DRF defaults leaking tracebacks | `core/exceptions.py` custom handler — all errors return the standard envelope |
| Pagination | No pagination | `StandardResultsPagination` on all list endpoints |
| Throttling | None | Configurable `anon` + `user` rate limits via `.env` |
| Logging | No logging | Structured rotating file logs (`logs/app.log`, `logs/error.log`) |
| CORS | None | `django-cors-headers` via `corsheaders` middleware |
| Static files | Not handled | `whitenoise` + `CompressedManifestStaticFilesStorage` |
| Health check | None | `GET /api/health/` with DB connectivity probe |
| ASGI | No `asgi.py` | `asgi.py` added for async-capable deployment |
| Tests | None | 60+ pytest tests covering all endpoints and validation rules |
| Indexes | No extra DB indexes | `db_index=True` on `code`, `is_active`, `primary_mapping` + composite indexes on mappings |
| Admin | Basic `list_display` | `BaseModelAdmin` / `BaseMappingAdmin` with bulk actions |
| Dev tooling | None | `Makefile`, `pytest.ini`, `.gitignore`, `.env.example` |
| Production server | `runserver` only | `gunicorn` config via `make serve` |

---

## Tech Stack

| Layer | Library |
|---|---|
| Language | Python 3.10+ |
| Framework | Django 4.2 |
| API | Django REST Framework 3.14 |
| Docs | drf-yasg (Swagger + ReDoc) |
| Config | django-environ |
| CORS | django-cors-headers |
| Static | whitenoise |
| Server | gunicorn |
| Tests | pytest + pytest-django |
| Database | SQLite (dev) / any Django-supported DB (prod) |

---

## Project Structure

```
modular_entity_system/
│
├── Makefile
├── manage.py
├── pytest.ini
├── requirements.txt
├── .env.example
├── .gitignore
│
├── modular_entity_system/          # Django project config
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── settings/
│       ├── base.py                 # All shared settings
│       ├── development.py          # Dev overrides (DEBUG=True, loose security)
│       └── production.py          # Prod hardening (HSTS, SSL redirect, etc.)
│
├── core/                           # Shared infrastructure (no business logic)
│   ├── models.py                   # TimestampedModel, MasterModel, MappingModel
│   ├── serializers.py              # BaseMasterSerializer, BaseMappingSerializer
│   ├── mixins.py                   # MasterEntityMixin, MappingEntityMixin
│   ├── helpers.py                  # Response helpers, get_object_or_error
│   ├── pagination.py               # StandardResultsPagination
│   ├── filters.py                  # Queryset filter helpers
│   ├── exceptions.py               # Custom DRF exception handler + ApplicationError
│   ├── swagger.py                  # Reusable openapi schema factory functions
│   ├── admin.py                    # BaseModelAdmin, BaseMappingAdmin
│   ├── views.py                    # HealthCheckView
│   └── urls.py                     # /api/health/
│
├── vendor/                         # ← Master entity (30 lines of actual logic)
├── product/                        # ← Master entity
├── course/                         # ← Master entity
├── certification/                  # ← Master entity
│
├── vendor_product_mapping/         # ← Mapping entity
├── product_course_mapping/         # ← Mapping entity
├── course_certification_mapping/   # ← Mapping entity
│
├── tests/
│   ├── conftest.py                 # Shared pytest fixtures
│   ├── test_health.py
│   ├── test_vendor.py              # Full CRUD + validation (18 tests)
│   ├── test_master_entities.py     # Products, Courses, Certifications + pagination
│   ├── test_vendor_product_mapping.py  # Mapping CRUD + all constraints (20 tests)
│   ├── test_product_course_mapping.py
│   └── test_course_certification_mapping.py
│
└── logs/                           # Created automatically at runtime
    ├── app.log                     # Rotating — INFO+ from 'app' logger
    └── error.log                   # Rotating — ERROR+ from all loggers
```

---

## Quick Start

### 1. Set up environment

```bash
git clone <repo-url>
cd modular_entity_system

python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

make install
make env                       # creates .env from .env.example
```

Edit `.env` — at minimum set `SECRET_KEY`:
```
SECRET_KEY=your-very-long-random-secret-key-here
```

### 2. Run migrations

```bash
make migrations
make migrate
```

### 3. (Optional) Create admin superuser

```bash
make superuser
```

### 4. Start the server

```bash
make run
# → http://127.0.0.1:8000/
```

### 5. Run tests

```bash
make test
```

---

## API Endpoints

### System

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health/` | Health check — DB connectivity probe |
| GET | `/swagger/` | Interactive Swagger UI |
| GET | `/redoc/` | ReDoc documentation |

### Master Entities

All four master entities share the same URL pattern.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/vendors/` | List (paginated, filterable) |
| POST | `/api/vendors/` | Create |
| GET | `/api/vendors/<id>/` | Retrieve |
| PUT | `/api/vendors/<id>/` | Full update |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Soft delete |

Same pattern for `/api/products/`, `/api/courses/`, `/api/certifications/`.

### Mapping Entities

| Method | Endpoint |
|---|---|
| GET / POST | `/api/vendor-product-mappings/` |
| GET / PUT / PATCH / DELETE | `/api/vendor-product-mappings/<id>/` |
| GET / POST | `/api/product-course-mappings/` |
| GET / PUT / PATCH / DELETE | `/api/product-course-mappings/<id>/` |
| GET / POST | `/api/course-certification-mappings/` |
| GET / PUT / PATCH / DELETE | `/api/course-certification-mappings/<id>/` |

---

## Query Parameters

### Filtering

| Endpoint | Param | Example |
|---|---|---|
| All lists | `is_active` | `?is_active=true` |
| `/api/products/` | `vendor_id` | `?vendor_id=1` |
| `/api/courses/` | `product_id` | `?product_id=2` |
| `/api/certifications/` | `course_id` | `?course_id=3` |
| Mapping lists | `primary_mapping` | `?primary_mapping=true` |
| `/api/vendor-product-mappings/` | `vendor_id`, `product_id` | `?vendor_id=1` |
| `/api/product-course-mappings/` | `product_id`, `course_id` | `?product_id=2` |
| `/api/course-certification-mappings/` | `course_id`, `certification_id` | `?course_id=3` |

### Pagination

All list endpoints are paginated:

```
?page=1&page_size=20
```

Response shape:
```json
{
  "success": true,
  "message": "Results retrieved successfully.",
  "data": {
    "count": 42,
    "total_pages": 3,
    "current_page": 1,
    "next": "http://localhost:8000/api/vendors/?page=2",
    "previous": null,
    "results": [ ... ]
  }
}
```

---

## Response Envelope

Every response — success or failure — uses the same shape:

```json
{
  "success": true | false,
  "message": "Human readable status",
  "data": { ... } | [ ... ] | null,
  "errors": { ... }   // only present on 400 responses
}
```

### Status Codes

| Code | When |
|---|---|
| 200 | GET / PUT / PATCH success |
| 201 | POST created |
| 204 | DELETE soft-deleted |
| 400 | Validation error / bad request |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Unexpected server error |
| 503 | Health check — DB unreachable |

---

## Validation Rules

### Master entities
- `name` required, non-blank
- `code` required, unique per model, auto-uppercased

### Mapping entities
- Both FK targets must exist **and** be `is_active=True`
- The `(parent, child)` pair is unique — duplicates return HTTP 400
- Only one `primary_mapping=True` per parent — a second returns HTTP 400

---

## Logging

Logs are written to `logs/` (created automatically):

```bash
make logs          # tail -f logs/app.log
```

The application logger name is `app`. Use it in any module:
```python
import logging
logger = logging.getLogger('app')
logger.info('Something happened: %s', value)
```

---

## Production Deployment

```bash
# Set environment
export DJANGO_SETTINGS_MODULE=modular_entity_system.settings.production
export SECRET_KEY=<your-secret>
export DATABASE_URL=postgres://user:pass@host:5432/dbname
export ALLOWED_HOSTS=yourdomain.com
export CORS_ALLOWED_ORIGINS=https://yourfrontend.com

# Collect static files
python manage.py collectstatic --noinput

# Start gunicorn (or use make serve)
make serve
```

---

## Architecture Notes

### Why `core/mixins.py` instead of ViewSets?

ViewSets require Routers, which generate URLs automatically and reduce
transparency. The `MasterEntityMixin` and `MappingEntityMixin` give us the
same DRY benefit (write CRUD logic once) while keeping every URL explicitly
declared and every HTTP method explicitly dispatched — exactly what `APIView`
is designed for.

### Why split settings files?

A single `settings.py` with `if DEBUG:` branches is hard to audit and easy to
misconfigure. Split files make it impossible to accidentally deploy
development settings to production: the `DJANGO_SETTINGS_MODULE` env var is
the gating mechanism.

### Why `soft_delete()` instead of `DELETE`?

Hard deletes in a relational system are destructive and irreversible. Soft
deletes (`is_active=False`) preserve audit history and allow recovery. Cascade
integrity is maintained by `on_delete=PROTECT` on all FK fields — you cannot
delete a parent that still has active children.
