from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    is_admin: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    user_id: int 

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True