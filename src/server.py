"""Local development server with custom endpoints"""
from fastapi import FastAPI
from src.custom_endpoints import router
from src.app_config import configure_app

app = FastAPI()

# Configure app (exception handlers, middleware, etc.)
configure_app(app)

# Include custom endpoints
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
