from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError

from app.models.parent_chunk import ParentChunk
from app.schemas.parent_chunk import ParentChunkCreate, ParentChunkUpdate


class ParentChunkService:
    """Service class for parent chunk operations"""
    
    @staticmethod
    async def create(db: AsyncSession, chunk_data: ParentChunkCreate) -> ParentChunk:
        """
        Create a new parent chunk.
        
        Args:
            db: Database session
            chunk_data: Parent chunk creation data
            
        Returns:
            Created ParentChunk instance
            
        Raises:
            IntegrityError: If duplicate content_hash exists
        """
        chunk = ParentChunk(**chunk_data.model_dump())
        db.add(chunk)
        await db.commit()
        await db.refresh(chunk)
        return chunk
    
    @staticmethod
    async def get_by_id(db: AsyncSession, chunk_id: UUID) -> Optional[ParentChunk]:
        """
        Get parent chunk by ID.
        
        Args:
            db: Database session
            chunk_id: UUID of the parent chunk
            
        Returns:
            ParentChunk instance or None
        """
        result = await db.execute(
            select(ParentChunk).where(ParentChunk.id == chunk_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_content_hash(db: AsyncSession, content_hash: str) -> Optional[ParentChunk]:
        """
        Get parent chunk by content hash (for deduplication).
        
        Args:
            db: Database session
            content_hash: SHA-256 hash of content
            
        Returns:
            ParentChunk instance or None
        """
        result = await db.execute(
            select(ParentChunk).where(ParentChunk.content_hash == content_hash)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_by_ids(db: AsyncSession, chunk_ids: List[UUID]) -> List[ParentChunk]:
        """
        Get multiple parent chunks by IDs (bulk retrieval for vector search results).
        
        Args:
            db: Database session
            chunk_ids: List of chunk UUIDs
            
        Returns:
            List of ParentChunk instances
        """
        result = await db.execute(
            select(ParentChunk).where(ParentChunk.id.in_(chunk_ids))
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_all(
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        order_by_index: bool = True
    ) -> List[ParentChunk]:
        """
        Get all parent chunks with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by_index: Whether to order by chunk_index
            
        Returns:
            List of ParentChunk instances
        """
        query = select(ParentChunk)
        
        if order_by_index:
            query = query.order_by(ParentChunk.chunk_index)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def update(
        db: AsyncSession, 
        chunk_id: UUID, 
        update_data: ParentChunkUpdate
    ) -> Optional[ParentChunk]:
        """
        Update a parent chunk.
        
        Args:
            db: Database session
            chunk_id: UUID of the chunk to update
            update_data: Update data
            
        Returns:
            Updated ParentChunk instance or None if not found
        """
        chunk = await ParentChunkService.get_by_id(db, chunk_id)
        if not chunk:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(chunk, field, value)
        
        await db.commit()
        await db.refresh(chunk)
        return chunk
    
    @staticmethod
    async def delete(db: AsyncSession, chunk_id: UUID) -> bool:
        """
        Delete a parent chunk.
        
        Args:
            db: Database session
            chunk_id: UUID of the chunk to delete
            
        Returns:
            True if deleted, False if not found
        """
        chunk = await ParentChunkService.get_by_id(db, chunk_id)
        if not chunk:
            return False
        
        await db.delete(chunk)
        await db.commit()
        return True
    
    @staticmethod
    async def exists_by_hash(db: AsyncSession, content_hash: str) -> bool:
        """
        Check if a chunk with given content hash already exists.
        
        Args:
            db: Database session
            content_hash: SHA-256 hash of content
            
        Returns:
            True if exists, False otherwise
        """
        chunk = await ParentChunkService.get_by_content_hash(db, content_hash)
        return chunk is not None
