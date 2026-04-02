# Historical Ads Backend API

FastAPI backend for searching and analyzing historical job listings from the Swedish Public Employment Service (Arbetsförmedlingen).

## API Endpoints

| Endpoint | Metod | Beskrivning |
|----------|-------|-------------|
| `/api/v1/search` | GET | Search historical job listings |
| `/api/v1/search/ad/{id}` | GET | Retrieve a specific listing |
| `/api/v1/stats` | GET | Get statistics |
| `/api/v1/filters` | GET | Retrieve filter options |
| `/api/v1/export` | GET | Export data (JSON/CSV/XLSX) |
| `/health` | GET | Health check |

## Getting Started

## Production or minimal install. (Same as docker is using)

```bash
pip install -r requirements.txt
```

## Development install. (Developer tools like pytest and ruff)

```bash
pip install -r requirements-dev.txt
```

## Start the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

## Code style (Ruff)

Configuration lives in `pyproject.toml` (shared by everyone and CI). After a dev install:

```bash
# Check for lint issues.
ruff check .

# Check and fix lint issues.
ruff check . --fix

# Check for format issues.
ruff format --check .

# Use ruff to format all files.
ruff format .

# Use ruff to format a specific file.
ruff format path/to/file.py
```

Use `ruff check . --fix` and `ruff format .` when you intentionally apply fixes. In CI, prefer check-only so main stays predictable.

For more information on the configuration check the [ruff rule documentation](https://docs.astral.sh/ruff/rules/).

## Docker

```bash
# Start the API using Docker Compose
docker compose up --build

# Access the API at http://localhost:5000

# Stop the server
docker compose down
```


## API Documentation

- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
