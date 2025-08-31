from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)
# Executar no terminal, para iniciar o servidor FastAPI: uvicorn main:app --reload
