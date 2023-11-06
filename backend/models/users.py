from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str
    password2: str
    

class User(UserBase):
    id: int
    player_id: Optional[int]


class PlayerProfile(BaseModel):
    id: int
    full_name: str
    country: str
    sports_club: str