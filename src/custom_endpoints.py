"""Custom API endpoints for LangSmith deployment"""
from fastapi import APIRouter
from src.controllers.documents import router as documents_router
from src.controllers.chats import router as chats_router

# Main router that combines all custom endpoints
router = APIRouter()

router.include_router(documents_router)
router.include_router(chats_router)
