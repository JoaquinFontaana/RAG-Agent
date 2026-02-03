from src.models.entities.User import User
from src.dtos.user import UserCreate
from src.db import engine
from sqlmodel import Session, select
from fastapi import HTTPException
from src.security.hash import hash_password
class UserService:

    def create_user(self,user_data:UserCreate):
        if self.exist_by_email(user_data.email):
            raise HTTPException(status_code=400,detail="The email already exists")
        
        user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )    
        self.save(user)
         
        
    def save(self,user:User):
        with Session(engine) as session:
            session.add(user)
            session.commit()

    def find_by_id(self,id:int) -> User:
        with Session(engine) as session:
            user = session.exec(select(User).where(User.id == id)).first()
        if not user:
            raise HTTPException(status_code=404,detail="The user doesnt exists")
        return user
    
    def find_by_email(self,email:str) -> User:
        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            raise HTTPException(status_code=404,detail="The user doesnt exists")
        return user

    def exist_by_email(self, email: str) -> bool:
        with Session(engine) as session:
            return session.exec(select(User).where(User.email == email)).first() is not None
