from sqlalchemy.ext.declarative import declarative_base

# Create Base class for models
Base = declarative_base()

# Import all models here so Alembic can detect them
# This ensures all models are registered with Base.metadata
# Note: Import models ONLY when needed for migrations, not during app startup
# from app.models.example import Example  # noqa
