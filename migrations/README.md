# Database Migrations

This directory contains SQL migration files for the database schema.

## Running Migrations

### Option 1: Using psql (Direct SQL)

```bash
# Connect to your PostgreSQL database and run the migration
psql -U your_username -d your_database -f migrations/001_create_parent_chunks_table.sql
```

### Option 2: Using Docker (if using docker-compose)

```bash
# Copy the migration file into the container and run it
docker-compose exec db psql -U your_username -d your_database -f /path/to/migration.sql
```

### Option 3: Using Python script

```python
from app.db.session import engine
import asyncio

async def run_migration():
    async with engine.begin() as conn:
        with open('migrations/001_create_parent_chunks_table.sql', 'r') as f:
            sql = f.read()
            await conn.execute(text(sql))

asyncio.run(run_migration())
```

## Migration Files

- `001_create_parent_chunks_table.sql` - Creates the parent_chunks table for RAG system

## Future: Alembic Setup

If you want to use Alembic for migrations in the future, you can initialize it with:

```bash
alembic init alembic
```

Then configure it to use your database and models.
