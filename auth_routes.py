from fastapi import APIRouter, Depends 
from main import bcrypt_context
from models import User
from dependencies import get_session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    This route is used to check if the user is authenticated
    """
    return {"message": "You are on the login route", "authenticated": False}

@auth_router.post("/create")
async def create_user(email:str, password:str, name:str, session = Depends(get_session)):

    user = session.query(User).filter(User.email == email).first()
    if user:
        return {"message": "Alredy exist a user with this email"} 
    else:
        crypt_password = bcrypt_context.hash(password)
        new_user = User(name= name, email= email, password= crypt_password)
        session.add(new_user)
        session.commit()
        return {"message": "User add with sucess!"}
        