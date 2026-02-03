from fastapi import Depends
from fastapi.routing import APIRouter
from src.dtos.user import UserCreate
from src.services.user_service import UserService
from src.dependencies import get_user_service
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users")


@router.post("", status_code=201)
def create_user(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    service.create_user(user_data)
    return JSONResponse({
        "message": "User created sucessfull"
    })