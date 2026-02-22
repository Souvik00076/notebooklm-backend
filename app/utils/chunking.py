import hashlib
from typing import Dict, Any, Optional


def generate_content_hash(content: str) -> str:
    """
    Generate SHA-256 hash of content for deduplication.
    
    Args:
        content: The text content to hash
        
    Returns:
        64-character hexadecimal SHA-256 hash
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def calculate_char_count(content: str) -> int:
    """
    Calculate character count of content.
    
    Args:
        content: The text content
        
    Returns:
        Number of characters
    """
    return len(content)


def prepare_parent_chunk_data(
    content: str,
    chunk_index: int,
    token_count: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Prepare parent chunk data for database insertion.
    
    Args:
        content: The parent chunk text content
        chunk_index: Position/order of chunk in sequence
        token_count: Optional token count
        metadata: Optional metadata dictionary
        
    Returns:
        Dictionary with all required fields for ParentChunkCreate schema
    """
    return {
        "content": content,
        "content_hash": generate_content_hash(content),
        "chunk_index": chunk_index,
        "token_count": token_count,
        "char_count": calculate_char_count(content),
        "metadata": metadata or {}
    }
