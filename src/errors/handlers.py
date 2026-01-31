from fastapi import Request, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.errors.exceptions import BaseAppException
import logging

logger = logging.getLogger(__name__)

# 1. Handler para TUS errores de lógica
async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

# 2. Handler para errores HTTP estándar de FastAPI (404, 401, etc)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": "HTTPException",
                "message": exc.detail
            }
        }
    )

# Handler para validaciones de Pydantic (Datos mal enviados)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join([str(x) for x in error["loc"][1:]])
        msg = error["msg"]
        errors.append(f"{field}: {msg}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "type": "ValidationError",
                "message": "Error de validación en los datos enviados",
                "details": errors
            }
        }
    )

#Handler GENÉRICO 
async def general_exception_handler(request: Request, exc: Exception):
    # Logueamos el error real en el servidor para que tú lo veas
    logger.error(f"Error no controlado: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "type": "InternalServerError",
                "message": "Ha ocurrido un error inesperado en el servidor."
            }
        }
    )

# Setup function to register all handlers
def setup_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers to the FastAPI app"""
    app.add_exception_handler(BaseAppException, app_exception_handler)  # type: ignore
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
    app.add_exception_handler(Exception, general_exception_handler)  # type: ignore