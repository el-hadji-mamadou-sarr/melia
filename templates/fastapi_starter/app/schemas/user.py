from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSchema(BaseModel):
    id: int
    nom: str
    email: EmailStr
    phone: Optional[str] = None
    avatar: Optional[str] = None
    is_owner: bool
    is_passenger: bool

    class Config:
        from_attributes = True

class UserRegisterSchema(BaseModel):
    nom: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    is_owner: bool
    is_passenger: bool

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
