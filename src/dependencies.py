from fastapi import Depends
from src.services.user_service import UserService
from src.services.auth_service import AuthService


def get_user_service() -> UserService:
    """Dependency para inyectar UserService"""
    return UserService()


def get_auth_service(
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    """Dependency para inyectar AuthService con UserService"""
    return AuthService(user_service)
