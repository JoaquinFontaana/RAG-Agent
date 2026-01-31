"""Application configuration for LangSmith deployment"""
from fastapi import FastAPI
from src.errors.handlers import setup_exception_handlers
import logging

logger = logging.getLogger(__name__)

def configure_app(app: FastAPI) -> None:
    """
    Configure the FastAPI application with handlers, middleware, etc.
    This is called by LangSmith during deployment.
    """
    logger.info("Configuring FastAPI application...")
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Add any other configuration here
    # - CORS middleware
    # - Additional middleware
    # - Startup/shutdown events
    
    logger.info("Application configured successfully")
