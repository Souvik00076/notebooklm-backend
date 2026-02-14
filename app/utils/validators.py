from typing import Any
import re


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
    
    Returns:
        True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_file_size(file_size: int, max_size: int) -> bool:
    """
    Validate file size.
    
    Args:
        file_size: Size of file in bytes
        max_size: Maximum allowed size in bytes
    
    Returns:
        True if file size is within limit, False otherwise
    """
    return file_size <= max_size


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """
    Validate file extension.
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions (e.g., ['.pdf', '.txt'])
    
    Returns:
        True if extension is allowed, False otherwise
    """
    extension = filename.lower().split('.')[-1]
    return f'.{extension}' in [ext.lower() for ext in allowed_extensions]


def sanitize_string(text: str) -> str:
    """
    Sanitize string by removing potentially harmful characters.
    
    Args:
        text: String to sanitize
    
    Returns:
        Sanitized string
    """
    # Remove any HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove any script tags
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()
