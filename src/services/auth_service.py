from src.services.user_service import UserService
from src.dtos.login_request import LoginRequest
from src.security.jwt import create_access_token
from src.security.hash import verify_password
from fastapi import HTTPException, status


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        
    def login(self, credentials: LoginRequest) -> str:
        user = self.user_service.find_by_email(credentials.email)
        
        if not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        return create_access_token({
            "role": user.role.name,
            "sub": str(user.id)
        })