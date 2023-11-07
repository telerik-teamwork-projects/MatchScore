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
    player_id: Optional[int]

class UserLoginResponse(BaseModel):
    token: str
    user: User

class PlayerProfile(BaseModel):
    id: int
    full_name: str
    country: str
    sports_club: str