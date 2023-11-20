from pydantic import BaseModel
from typing import Optional
from models.enums import Role
from models.players import PlayerProfile

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


class UserWithPlayer(User):
    player: Optional[PlayerProfile] = None

    @classmethod
    def from_query_result(cls, id, username, email, role, bio, profile_img, cover_img, player_id=None, full_name=None, country=None, sports_club=None):
        if player_id:
            user_with_player = cls(
                id=id,
                username=username,
                email=email,
                role=role,
                bio=bio,
                profile_img=profile_img,
                cover_img=cover_img,
                player=PlayerProfile.from_query_result(
                    id=player_id,
                    full_name=full_name,
                    country=country,
                    sports_club=sports_club,
                )
            )
        else:
            user_with_player = cls(
                id=id,
                username=username,
                email=email,
                role=role,
                bio=bio,
                profile_img=profile_img,
                cover_img=cover_img,
                player=None
            )

        return user_with_player



class UserLoginResponse(BaseModel):
    token: str
    user: User


class LinkToPlayerCreate(BaseModel):
    full_name:str