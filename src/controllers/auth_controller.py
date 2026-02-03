from fastapi import APIRouter, Depends
from src.dtos.login_request import LoginRequest
from src.dependencies import get_auth_service
from src.services.auth_service import AuthService
router = APIRouter(prefix="/auth")

@router.post("/login")
def login(credentials: LoginRequest, service: AuthService = Depends(get_auth_service)):
    token = service.login(credentials)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout():