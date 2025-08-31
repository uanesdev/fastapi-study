from fastapi import APIRouter, Depends 
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
    # Esse método possui alguns problemas:
    # 1 - A Session iniciada não nescessáriamente é fechada (várias conexões com o DB podem gerar erro)
    # 2 - Simplismente estamos retornando mensagens (devemos retornar os códigos HTTP(2XX, 4XX))
    # 3 - Os parametros estão de forma despradronizada (podemos simplismente pedir uma instância de User)
    # 4- Senha não esta criptpgrafada
    # 5 - As responsabilidades não estão separadas

    user = session.query(User).filter(User.email == email).first()
    if user:
        return {"message": "Alredy exist a user with this email"} 
    else:
        new_user = User(name= name, email= email, password= password)
        session.add(new_user)
        session.commit()
        return {"message": "User add with sucess!"}
        