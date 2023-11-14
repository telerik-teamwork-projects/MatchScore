from pydantic import BaseModel
from typing import Optional
from models.enums import Request 

class TournamentRequest(BaseModel):
    id: int
    user_id: int
    tournament_id: int
    full_name: str
    country: Optional[str]
    sports_club: Optional[str]
    status: Request = Request.PENDING