from sqlmodel import Field, SQLModel, Relationship
from src.models.entities.Role import Role

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role:Role = Relationship()