from datetime import datetime
from pydantic import BaseModel
from typing import List
from models.enums import MatchFormat
from models.players import PlayerProfile


class MatchScore(BaseModel):
    match_id: int | None = None
    player: str | None = None
    score: int | None = None
    points: int | None = None

    @classmethod
    def from_query_result(cls, match_id, player, score=0, points=0):
        return cls(
            match_id=match_id,
            player=player,
            score=score,
            points=points)


class MatchDateUpdate(BaseModel):
    date: datetime


class MatchPlayerUpdate(BaseModel):
    player_id: int | None = None
    player: str
    player_prev: str


class MatchScoreUpdate(MatchPlayerUpdate):
    player_prev: str | None = None
    score: int
    points: int | None = None


class MatchBase(BaseModel):
    id: int | None = None
    date: datetime
    format: MatchFormat
    tournament_id: int | None = None
    next_match: int | None = None

    @classmethod
    def from_query_result(cls, id, date, format, tournament_id, next_match):
        return cls(
            id=id,
            date=date,
            format=format,
            tournament_id=tournament_id,
            next_match=next_match)


class Match(MatchBase):
    participants: List[PlayerProfile]

    @classmethod
    def from_query_result(cls, id, date, format, tournament_id, participants=None):
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
    score: List[MatchScore]

    @classmethod
    def from_query_result(cls, id, date, format, tournament_id, participants=None, score=None):
        if participants == '' or participants is None:
            participants = []
        else:
            participants = list(PlayerProfile.from_query_result(*row) for row in participants)
        if score == '' or score is None:
            score = []
        else:
            score = list(MatchScore.from_query_result(*row) for row in score)
        return cls(
            id=id,
            date=date,
            format=str(MatchFormat(format)),
            tournament_id=tournament_id,
            participants=participants,
            score=score)
