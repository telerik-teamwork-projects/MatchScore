from pydantic import BaseModel
from typing import Optional
from models.enums import Role

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
    

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None
    bio: Optional[str] = None
    profile_img: Optional[str] = None
    cover_img: Optional[str] = None
    # player_id: Optional[int]
    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    token: str
    user: User


class PlayerProfile(BaseModel):
    id: int | None = None
    full_name: str
    country: str | None = None
    sports_club: str | None = None

    @classmethod
    def from_query_result(cls, id, full_name, country=None, sports_club=None):
        return cls(
            id=id,
            full_name=full_name,
            country=country,
            sports_club=sports_club)
