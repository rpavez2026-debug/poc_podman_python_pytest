# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A QA-automation proof of concept: a small FastAPI service (`api/main.py`) backed by PostgreSQL, run with Podman, and tested black-box with pytest + `requests`. Code identifiers, API messages and test names are in Spanish (`usuarios`, `obtener_usuario`, `"Usuario no encontrado"`); keep that convention.

Note: there is no git repo scoped to this folder. The enclosing git repository is the user's home directory (`C:/Users/ricar`), so `git status`/commits from here operate on the whole home dir.

## Architecture

- **API** (`api/`): a single FastAPI app. `/health` is static; `/usuarios/{usuario_id}` opens a new `psycopg` (v3) connection per request using `DB_CONFIG`, built from the env vars `DB_HOST` (default `qa-postgres`), `DB_PORT` (5432), `DB_NAME` (`qa_database`), `DB_USER` (`qa_user`) and `DB_PASSWORD`. `POST /usuarios` takes a `UsuarioCrear` body (`email` is an `EmailStr`, which needs `email-validator`) and returns 201 with the new id. If the email is already registered it returns 409, which needs a UNIQUE constraint on `usuarios.email`. Error contract: a non-int id gives a 422 from FastAPI validation, a missing row gives a 404 `"Usuario no encontrado"`, and any `psycopg.Error` gives a 503 `"Base de datos no disponible"`.
- **Containerfile**: builds the API image (python:3.12-slim, uvicorn on port 8000). Only `api/` is copied into the image.
- **compose.yaml**: defines **only** the Postgres service (container `qa-postgres`, host port **5433** → 5432, credentials `qa_user` / `qa_password_local` / `qa_database`, named volume `postgres_data`). The API is not in compose. To reach `qa-postgres` by name, run the API container on the compose network. A host-run API needs `DB_HOST=127.0.0.1 DB_PORT=5433`.
- **Database schema/seed**: `database/` is empty. Nothing creates the `usuarios` table (`id, nombre, email, activo`), so set it up by hand. The tests expect row `id=1` to be `nombre='Usuario QA'`, `email='qa@test.com'`, `activo=true`, and id `999999` must not exist.
- **Tests** (`tests/`): pure HTTP tests against a running API. Nothing is imported from `api/` and there are no fixtures or conftest. Each file targets a different port:
  - `test_api.py` → `http://127.0.0.1:8000`
  - `test_api_postgres.py` → `http://127.0.0.1:8001`

  So the API is expected to be published on 8000 and/or 8001 when running the matching suite. `test_api.py::test_consultar_usuario` also needs the DB.

## Commands

```bash
# Start Postgres
podman compose up -d

# Build the API image
podman build -t poc-api -f Containerfile .

# Run the API (publish to 8000 or 8001 to match the test file; attach to the compose network, pass DB_PASSWORD)
podman run -d -p 8001:8000 --network <compose_network> -e DB_PASSWORD=qa_password_local poc-api

# Or run the API locally without a container
pip install -r api/requirements.txt
cd api && DB_HOST=127.0.0.1 DB_PORT=5433 DB_PASSWORD=qa_password_local uvicorn main:app --port 8000

# Tests (pytest and requests are not in requirements.txt; install them on the host)
pip install pytest requests
pytest tests/
pytest tests/test_api_postgres.py
pytest "tests/test_api.py::test_usuario_id_invalido[abc]"
```

There is no linter, formatter or pytest config in the project.
