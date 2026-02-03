from typing import TypedDict
from datetime import datetime
class TokenPayload(TypedDict):
    sub:str
    exp:datetime
    iat:datetime
    role:str