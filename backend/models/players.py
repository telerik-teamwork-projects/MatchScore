from pydantic import BaseModel
from typing import Optional
from models.enums import Request
from models.pagination import Pagination


class PlayerProfile(BaseModel):
    id: int | None = None
    full_name: str
    country: str | None = None
    sports_club: str | None = None
    user_id: Optional[int] = None

    @classmethod
    def from_query_result(cls, id, full_name, country=None, sports_club=None, user_id=None):
        return cls(
            id=id,
            full_name=full_name,
            country=country,
            sports_club=sports_club,
            user_id=user_id
        )


class PlayerCreate(BaseModel):
    user_id: Optional[int] = None
    full_name: str
    country: Optional[str] = None
    sports_club: Optional[str] = None


class PlayerRequest(BaseModel):
    id: int
    requester_id: int
    full_name: str
    country: Optional[str]
    sports_club: Optional[str]
    status: Request = Request.PENDING


class PlayerProfileImg(BaseModel):
    id: int | None = None
    full_name: str
    country: str | None = None
    sports_club: str | None = None
    profile_img: Optional[str] = None

    @classmethod
    def from_query_result(cls, id, full_name, country=None, sports_club=None, profile_img=None):
        return cls(
            id=id,
            full_name=full_name,
            country=country,
            sports_club=sports_club,
            profile_img=profile_img
        )


class PaginatedPlayers(BaseModel):
    players: list[PlayerProfileImg]
    pagination: Pagination
