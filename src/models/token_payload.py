from typing import TypedDict
from datetime import datetime
from src.models.entities.Role import RoleEnum
class TokenPayload(TypedDict):
    sub:str
    exp:datetime
    iat:datetime
    role:RoleEnum