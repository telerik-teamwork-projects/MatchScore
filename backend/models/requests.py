from pydantic import BaseModel
from typing import Optional
from models.enums import TournamentRequest 

class TournamentRequest(BaseModel):
    id: int
    user_id: int
    tournament_id: int
    full_name: str
    country: Optional[str]
    sports_club: Optional[str]
    status: TournamentRequest = TournamentRequest.PENDING