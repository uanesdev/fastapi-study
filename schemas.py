from pydantic import BaseModel
from typing import Optional

class UserSchema():
    name: str
    email: str
    password: str
    is_admin: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
        