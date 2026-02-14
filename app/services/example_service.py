from sqlalchemy.orm import Session
from sqlalchemy.future import select
from typing import List, Optional

from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleUpdate


class ExampleService:
    """
    Service class for handling business logic related to Example model.
    This is a dummy service to demonstrate the service layer pattern.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Example]:
        """Get all examples with pagination"""
        result = await self.db.execute(
            select(Example).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_id(self, example_id: int) -> Optional[Example]:
        """Get example by ID"""
        result = await self.db.execute(
            select(Example).where(Example.id == example_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, example_data: ExampleCreate) -> Example:
        """Create a new example"""
        example = Example(**example_data.model_dump())
        self.db.add(example)
        await self.db.commit()
        await self.db.refresh(example)
        return example
    
    async def update(self, example_id: int, example_data: ExampleUpdate) -> Optional[Example]:
        """Update an existing example"""
        example = await self.get_by_id(example_id)
        
        if not example:
            return None
        
        # Update only provided fields
        update_data = example_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(example, field, value)
        
        await self.db.commit()
        await self.db.refresh(example)
        return example
    
    async def delete(self, example_id: int) -> bool:
        """Delete an example"""
        example = await self.get_by_id(example_id)
        
        if not example:
            return False
        
        await self.db.delete(example)
        await self.db.commit()
        return True
