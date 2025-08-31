from jose import JWTError, jwt  # pyright: ignore[reportMissingModuleSource]
from fastapi import Depends, HTTPException  # pyright: ignore[reportMissingImports]
from main import ALGORITHM, SECRET_KEY, oauth2_schema
from models import User, db
from sqlalchemy.orm import Session, sessionmaker

# Garante que a session é fechada!
def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        info_dict = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(info_dict.get("sub"))
    except JWTError as error:
        print(error)
        raise HTTPException(status_code=401, detail= "Unauthorized. Please verify the validity of the token")

    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail= "Invalid Access")
    return user