from fastapi import APIRouter
from app.api.v1.endpoints import example, upload

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(example.router)
api_router.include_router(upload.router)

# Add more routers here as you create them:
# api_router.include_router(notebooks.router)
# api_router.include_router(sources.router)
# api_router.include_router(chat.router)
