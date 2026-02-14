from typing import Generator
from app.db.session import SessionLocal


async def get_db() -> Generator:
    """
    Dependency function that yields database sessions.
    Use this in your endpoint functions to get a database session.
    
    Example:
        @router.get("/items")
        async def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
