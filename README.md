# Mutuo Backend

Backend API for **Mutuo**, a property rental management platform that connects owners (*propietarios*) and tenants (*inquilinos*) around property listings and rental contracts.

Built with **FastAPI** and **async SQLAlchemy**, structured as a set of independent domain modules following **hexagonal / ports-and-adapters architecture** — business logic is fully decoupled from the web framework, the database, and third-party services, and is exercised by unit tests without touching a real database.

## Overview

Mutuo lets owners list properties, manage their portfolio, and issue rental contracts against those listings, while tenants authenticate and browse. The API covers:

- **Auth** — registration gated by email verification codes, session-cookie login (Redis-backed opaque sessions), logout, password change (via current password or a verification code for account recovery), and email change — all with attempt limits and temporary lockouts.
- **Users** — profile management for two profile types: `PROPIETARIO` (owner) and `INQUILINO` (tenant).
- **Listings** — CRUD for property listings owned by a user, with pagination and filtering.
- **Contracts** — rental contracts tied to a listing, with status and expiration tracking.

Cross-cutting concerns — caching, hashing/encryption, email delivery, rate limiting, and centralized error handling — are implemented once and shared across every domain.

## Architecture

Each business domain (`auth`, `users`, `listings`, `contracts`) is organized in layers, with the **use case layer depending only on abstract, function-shaped ports** — never on FastAPI, SQLAlchemy, or Redis directly. Concrete adapters are wired in at the edges via dependency injection.

```
Route (FastAPI)  →  Use case (pure business logic)  →  Port (Protocol / Callable type)
                                                              ↑
                                              Adapter (SQLAlchemy repository, Redis, SMTP, ...)
```

Per-module layout (using `listings` as the example):

```
mutuo/listings/
├── models.py               # Framework-agnostic domain entities (frozen dataclasses)
├── types.py                 # Ports: Callable/Protocol type aliases the use cases depend on
├── usecases.py               # Business logic — plain functions taking ports as arguments
├── schemas.py                # Pydantic request/response DTOs (the HTTP boundary)
├── mappers.py                 # domain ↔ schema translation
├── routes.py                   # FastAPI router — wires DTOs, use cases, and DI together
└── sqlalchemy/                  # Persistence adapter for this domain
    ├── models.py                    # ORM row definitions
    ├── repository.py                 # CRUD functions operating on ORM rows
    ├── mappers.py                     # ORM row ↔ domain model translation
    └── dependencies.py                 # FastAPI `Depends` providers exposing repository
                                          #   functions as the ports declared in types.py
```

Because use cases only ever see a `Protocol`/`Callable` port (e.g. `CreateListingFn`, `GetListingsByUserIdFn`), they're tested with plain fakes/stubs in-process — no test database, no HTTP client required for unit coverage of business rules. Route-level tests then verify the wiring end to end.

### Cross-cutting modules

| Module | Responsibility |
|---|---|
| `security/` | `CryptographyService` port + implementation: bcrypt password hashing, deterministic (searchable) hashing for indexed-but-sensitive fields like email, and Fernet-based encryption for PII at rest. |
| `cache/` | `CacheStore` port + Redis adapter: backs sessions, rate-limit counters, and verification-code/attempt tracking. |
| `communications/` | Email delivery (SMTP) and HTML template rendering for verification emails. |
| `database/` | Async SQLAlchemy engine/session factory and table management. |
| `exceptions.py` | A small domain exception hierarchy (`NotfoundException`, `UnauthorizedException`, `ForbiddenException`, `ConflictException`, `UnprocessableException`) mapped centrally to HTTP status codes. |
| `app/` | FastAPI app assembly: lifespan-managed shared services, middleware stack, and router aggregation. |

### Request pipeline (middleware stack)

Every request passes through, in order:

1. **CORS** — configurable allowed origins.
2. **`ExceptionHandler`** — catches domain exceptions and maps them to structured JSON errors via `ErrorSlug`; unexpected exceptions are logged and returned as a generic `500`.
3. **`RateLimiter`** — Redis-backed sliding window per client IP, with a temporary block once the limit is exceeded.
4. **DB session middleware** — opens an async SQLAlchemy session per request under `/api/v1`, commits on success, rolls back on failure, and always closes the connection.

### Data & security model

- Domain entities are immutable (`@dataclass(frozen=True)`) and contain no ORM or framework code.
- Emails are hashed deterministically for lookups and encrypted at rest — the plaintext is never stored searchable.
- Passwords are hashed with bcrypt; sessions are opaque IDs stored server-side in Redis (httponly, secure, `SameSite=Lax` cookies) rather than client-trusted tokens.
- Sensitive flows (registration, login, credential updates) are protected by verification codes with a max-attempt counter and temporary lockout, on top of the global IP rate limiter.

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Web framework | FastAPI, Uvicorn |
| Database | PostgreSQL via SQLAlchemy 2.0 (async) + asyncpg |
| Cache / sessions / rate limiting | Redis |
| Security | bcrypt (hashing), `cryptography` / Fernet (encryption) |
| Config | Pydantic Settings (`.env`-driven) |
| Testing | pytest, pytest-asyncio, pytest-cov |
| Tooling | uv (dependency & environment management), ruff (lint), mypy (types) |

## Project structure

```
mutuo/
├── app/            # FastAPI app: main, router aggregation, middleware, logging
├── auth/           # Sessions, login/registration, verification, credential updates
├── users/          # User domain
├── listings/       # Property listing domain
├── contracts/      # Rental contract domain
├── security/       # Hashing & encryption port + implementation
├── cache/          # Cache port + Redis implementation
├── communications/ # Email sending + templates
├── database/       # SQLAlchemy engine/session setup and table management
├── exceptions.py   # Domain exception hierarchy
└── settings.py     # Environment-driven app configuration
tests/              # Mirrors the domain structure — one usecase + route test per feature
```

## Getting started

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL and Redis instances (local or remote)

### Setup

```bash
uv sync
```

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/mutuo
REDIS_URL=redis://localhost:6379

MAILER_HOST=smtp.example.com
MAILER_PORT=587
MAILER_USER=user@example.com
MAILER_PASSWORD=changeme

ENCRYPTION_KEY=<fernet-key>
HMAC_KEY=<fernet-key>

ALLOW_ORIGINS=["http://localhost:3000"]
ENV=local
DEBUG=true
```

Create the database tables:

```bash
uv run python -m mutuo.database.sqlalchemy.management
```

Run the API:

```bash
uv run app
```

The app boots at `http://localhost:8000`; interactive API docs are available at `/docs` and `/redoc`.

### Testing

```bash
uv run pytest
```

Tests are organized per domain and per use case (e.g. `tests/listings/create/`, `tests/auth/login/`), each with a `test_usecase.py` (business logic against fakes) and `test_route.py` (HTTP wiring).

### Linting & type checking

```bash
uv run ruff check .
uv run mypy .
```
