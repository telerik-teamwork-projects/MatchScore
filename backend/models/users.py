from pydantic import BaseModel
from typing import Optional
from models.enums import Role

class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    password2: str


class UserLogin(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int
    role: Role = Role.USER
    bio: Optional[str] = None
    profile_img: Optional[str] = None
    cover_img: Optional[str] = None
    player_id: Optional[int] = None

    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    token: str
    user: User