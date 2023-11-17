from pydantic import BaseModel
from typing import Optional
from models.enums import Request 

from datetime import datetime

class TournamentRequest(BaseModel):
    id: int
    player_id: Optional[int]
    tournament_id: int
    user_id: Optional[int]
    full_name: str
    country: Optional[str]
    sports_club: Optional[str]
    status: Request = Request.PENDING
    created_at: datetime

    @classmethod
    def from_query_result(cls, id, player_id, tournament_id, user_id, full_name, country, sports_club, status, created_at):
        return cls(
            id=id,
            player_id=player_id,
            tournament_id=tournament_id,
            user_id=user_id,
            full_name=full_name,
            country=country,
            sports_club=sports_club,
            status=status,
            created_at=created_at
        )
    

class DirectorRequest(BaseModel):
    id: int
    user_id: int
    email: str
    status: Request = Request.PENDING
    created_at: datetime 

    @classmethod
    def from_query_result(cls, id, user_id, email, status, created_at):
        return cls(
            id=id,
            user_id=user_id,
            email=email,
            status=status,
            created_at=created_at
        )
    

class LinkToPlayerRequest(BaseModel):
    id: int
    user_id: int
    requested_full_name: str
    status: Request = Request.PENDING
    created_at: datetime

    @classmethod
    def from_query_result(cls, id, user_id, requested_full_name, status, created_at):
        return cls(
            id=id,
            user_id=user_id,
            requested_full_name=requested_full_name,
            status=status,
            created_at=created_at
        )
