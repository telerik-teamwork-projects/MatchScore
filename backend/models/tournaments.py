from pydantic import BaseModel
from typing import Optional

from models.enums import TournamentStatus, TournamentFormat, MatchFormat

class TournamentCreate(BaseModel):
    format: TournamentFormat = TournamentFormat.KNOCKOUT
    title: str
    match_format: MatchFormat = MatchFormat.TIME
    rounds: int
    third_place: bool
    status: TournamentStatus = TournamentStatus.OPEN
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    owner_id: int


class TournamentUpdate(BaseModel):
    format: Optional[str] = None
    title: Optional[str] = None
    match_format: Optional[str] = None
    rounds: Optional[int] = None
    third_place: Optional[bool] = None
    status: TournamentStatus = TournamentStatus.OPEN
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Owner(BaseModel):
    id: int
    username: str
    profile_img: str


class Tournament(BaseModel):
    id: int
    format: TournamentFormat = TournamentFormat.KNOCKOUT
    title: str
    match_format: MatchFormat = MatchFormat.TIME
    rounds: int
    third_place: bool
    status: TournamentStatus = TournamentStatus.OPEN
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    owner: Owner
    
