import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException

from app.utils.http_status import HTTPStatus
from app.schemas.upload import UploadResponse

router = APIRouter(prefix="/upload", tags=["upload"])

# Maximum file size: 1MB in bytes
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1MB = 1,048,576 bytes

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=UploadResponse, status_code=HTTPStatus.CREATED)
async def upload_file(
    file: UploadFile = File(..., description="File to upload (max 1MB)")
) -> UploadResponse:
    """
    Upload a file with maximum size of 1MB.
    - **file**: The file to upload (required)
    Returns:
    - Upload metadata including filename, size, path, and upload timestamp
    Raises:
    - 413 Payload Too Large: If file size exceeds 1MB
    - 400 Bad Request: If no file is provided or file is empty
    """

    # Check if filename is empty
    if not file.filename:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid file: filename is empty"
        )

    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    # Validate file size
    if file_size == 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="File is empty"
        )

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=HTTPStatus.PAYLOAD_TOO_LARGE,
            detail=f"File size ({file_size} bytes) exceeds maximum allowed size of {
                MAX_FILE_SIZE} bytes (1MB)"
        )

    # Generate unique filename to avoid conflicts
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    # Save file to disk
    try:
        with open(file_path, "wb") as f:
            f.write(file_content)
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )

    # Prepare response
    upload_response = UploadResponse(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        content_type=file.content_type or "application/octet-stream",
        uploaded_at=datetime.utcnow(),
        message="File uploaded successfully"
    )

    return upload_response


@router.get("/info")
async def get_upload_info():
    """
    Get information about upload configuration.

    Returns:
    - Maximum file size allowed
    - Upload directory path
    """
    return {
        "max_file_size_bytes": MAX_FILE_SIZE,
        "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024),
        "upload_directory": str(UPLOAD_DIR.absolute()),
        "allowed_methods": ["POST"]
    }
