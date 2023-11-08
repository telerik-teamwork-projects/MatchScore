from datetime import datetime
from pydantic import BaseModel
from typing import List
from models.enums import MatchFormat
from models.users import PlayerProfile


class Match(BaseModel):
    id: int | None = None
    date: datetime
    format: MatchFormat
    tournament_id: int | None = None
    participants: List[PlayerProfile]

    @classmethod
    def from_query_result(cls, id, date, format, tournament_id, participants):
        if participants == '' or participants is None:
            participants = []
        else:
            participants = list(PlayerProfile.from_query_result(*row) for row in participants)
        return cls(
            id=id,
            date=date,
            format=format,
            tournament_id=tournament_id,
            participants=participants)


class MatchResponse(Match):
    format: str

    @classmethod
    def from_query_result(cls, id, date, format, tournament_id, participants):
        if participants == '' or participants is None:
            participants = []
        else:
            participants = list(PlayerProfile.from_query_result(*row) for row in participants)
        return cls(
            id=id,
            date=date,
            format=str(MatchFormat(format)),
            tournament_id=tournament_id,
            participants=participants)
