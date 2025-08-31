from sqlalchemy import false
from sqlalchemy.orm import Session, session
from sqlalchemy.sql.functions import user
from fastapi import APIRouter, Depends, HTTPException
from main import SECRET_KEY, bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models import User
from dependencies import get_session, verify_token
from schemas import LoginSchema, UserSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id: int, duration_token: int = timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire_date = datetime.now(timezone.utc) + duration_token
    info_dict = {"sub": str(user_id), "exp": expire_date}
    encoded_jwt = jwt.encode(info_dict, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def auth_user(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user

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
        
# login -> email and password -> JWT token -> akldhahdalidhadpas
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = auth_user(email= login_schema.email, password= login_schema.password, session= session)

    if not user:
        raise HTTPException(status_code = 400, detail= "User not found or user not auth!")
    
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration_token= timedelta(days=7))
        return {
            "access_token": access_token,
            "refrash_token": refresh_token,
            "token_type": "Bearer"}

@auth_router.get("/refresh")
async def refresh_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
