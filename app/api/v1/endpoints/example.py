from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.example import ExampleCreate, ExampleUpdate, ExampleResponse
from app.services.example_service import ExampleService

router = APIRouter(prefix="/examples", tags=["examples"])


@router.get("/", response_model=List[ExampleResponse])
async def get_examples(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all examples with pagination.
    """
    service = ExampleService(db)
    examples = await service.get_all(skip=skip, limit=limit)
    return examples


@router.get("/{example_id}", response_model=ExampleResponse)
async def get_example(
    example_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific example by ID.
    """
    service = ExampleService(db)
    example = await service.get_by_id(example_id)
    
    if not example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found"
        )
    
    return example


@router.post("/", response_model=ExampleResponse, status_code=status.HTTP_201_CREATED)
async def create_example(
    example_data: ExampleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new example.
    """
    service = ExampleService(db)
    example = await service.create(example_data)
    return example


@router.put("/{example_id}", response_model=ExampleResponse)
async def update_example(
    example_id: int,
    example_data: ExampleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing example.
    """
    service = ExampleService(db)
    example = await service.update(example_id, example_data)
    
    if not example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found"
        )
    
    return example


@router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_example(
    example_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an example.
    """
    service = ExampleService(db)
    success = await service.delete(example_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found"
        )
    
    return None
