"""Local development server with custom endpoints"""
from fastapi import FastAPI
from src.app_config import configure_app
from fastapi import APIRouter
from src.controllers.document_controller import router as documents_router
from src.controllers.chat_controller import router as chats_router

# Main router that combines all coontrollers
router = APIRouter()

router.include_router(documents_router)
router.include_router(chats_router)

app = FastAPI()

# Configure app (exception handlers, middleware, etc.)
configure_app(app)

# Include custom endpoints
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
