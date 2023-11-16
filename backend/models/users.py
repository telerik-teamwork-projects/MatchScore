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


class User(BaseModel):
    id: int
    username: str
    email: str
    role: Role = Role.USER
    bio: Optional[str] = None
    profile_img: Optional[str] = None
    cover_img: Optional[str] = None

    @classmethod
    def from_query_result(cls, id, username, email, role, bio, profile_img, cover_img):
        return cls(
            id=id,
            username=username,
            email=email,
            role=role,
            bio=bio,
            profile_img=profile_img,
            cover_img=cover_img,
        )


    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    token: str
    user: User