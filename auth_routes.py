from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from main import bcrypt_context
from models import User
from dependencies import get_session
from schemas import UserSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    This route is used to check if the user is authenticated
    """
    return {"message": "You are on the login route", "authenticated": False}

@auth_router.post("/create")
async def create_user(user_schema: UserSchema, session: Session = Depends(get_session)):

    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail= "Alredy exist a user with this email") 
    else:
        crypt_password = bcrypt_context.hash(user_schema.password)
        new_user = User(name= user_schema.name, email= user_schema.email, password= crypt_password, is_admin= user_schema.is_admin, is_active= user_schema.is_active)
        session.add(new_user)
        session.commit()
        return {"message": f"User add with sucess! {user_schema.email}"}
        