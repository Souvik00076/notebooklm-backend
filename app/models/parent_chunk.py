from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
import uuid
from app.db.base import Base


class ParentChunk(Base):
    """
    Model for storing parent chunks used in RAG systems.
    Parent chunks contain the full context that will be retrieved,
    while embeddings are stored in a separate vector database.
    """
    __tablename__ = "parent_chunks"

    # Primary key - using UUID for better distribution and compatibility with vector DBs
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)

    # Content fields
    content = Column(Text, nullable=False,
                     comment="The actual parent chunk text content")
    content_hash = Column(String(64), nullable=False, index=True, unique=True,
                          comment="SHA-256 hash of content for deduplication")

    # Ordering and metrics
    chunk_index = Column(Integer, nullable=False, index=True,
                         comment="Position/order of this chunk in sequence")
    token_count = Column(Integer, nullable=True,
                         comment="Number of tokens in this chunk")
    char_count = Column(Integer, nullable=True,
                        comment="Character count of this chunk")

    # Flexible metadata storage
    metadata = Column(JSONB, nullable=True, default={},
                      comment="Flexible metadata like page numbers, section headers, etc.")

    # Timestamps
    created_at = Column(DateTime(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True),
                        onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<ParentChunk(id={self.id}, chunk_index={self.chunk_index}, chars={self.char_count})>"
