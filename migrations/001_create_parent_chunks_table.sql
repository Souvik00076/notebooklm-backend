-- Migration: Create parent_chunks table
-- Description: Creates the parent_chunks table for storing parent chunks in RAG system
-- Date: 2026-02-22

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create parent_chunks table
CREATE TABLE IF NOT EXISTS parent_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL UNIQUE,
    chunk_index INTEGER NOT NULL,
    token_count INTEGER,
    char_count INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_parent_chunks_content_hash ON parent_chunks(content_hash);
CREATE INDEX IF NOT EXISTS idx_parent_chunks_chunk_index ON parent_chunks(chunk_index);
CREATE INDEX IF NOT EXISTS idx_parent_chunks_id ON parent_chunks(id);
CREATE INDEX IF NOT EXISTS idx_parent_chunks_created_at ON parent_chunks(created_at);

-- Add comments for documentation
COMMENT ON TABLE parent_chunks IS 'Stores parent chunks for RAG system. Child chunk embeddings are stored in external vector database.';
COMMENT ON COLUMN parent_chunks.id IS 'Primary key UUID, also used as reference in vector database';
COMMENT ON COLUMN parent_chunks.content IS 'The actual parent chunk text content that will be retrieved';
COMMENT ON COLUMN parent_chunks.content_hash IS 'SHA-256 hash of content for deduplication';
COMMENT ON COLUMN parent_chunks.chunk_index IS 'Position/order of this chunk in sequence';
COMMENT ON COLUMN parent_chunks.token_count IS 'Number of tokens in this chunk';
COMMENT ON COLUMN parent_chunks.char_count IS 'Character count of this chunk';
COMMENT ON COLUMN parent_chunks.metadata IS 'Flexible metadata like page numbers, section headers, etc.';
COMMENT ON COLUMN parent_chunks.created_at IS 'Timestamp when chunk was created';
COMMENT ON COLUMN parent_chunks.updated_at IS 'Timestamp when chunk was last updated';
