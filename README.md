# NotebookLM API

FastAPI backend for a NotebookLM-like application.

## Features

- FastAPI framework with async support
- SQLAlchemy ORM with async SQLite (easy to switch to PostgreSQL later)
- Pydantic v2 for validation
- Alembic for database migrations
- Structured project layout

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
notebook-backend/
├── app/
│   ├── api/v1/          # API routes
│   ├── core/            # Core functionality
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── db/              # Database setup
│   └── utils/           # Utilities
├── alembic/             # Database migrations
├── .env                 # Environment variables
└── requirements.txt     # Dependencies
```

## Development

- Add new endpoints in `app/api/v1/endpoints/`
- Define schemas in `app/schemas/`
- Create models in `app/models/`
- Business logic goes in `app/services/`
