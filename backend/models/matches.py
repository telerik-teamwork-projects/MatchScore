from datetime import datetime
from pydantic import BaseModel
from typing import List
from models.enums import MatchFormat
from models.pagination import Pagination
from models.players import PlayerProfile


class MatchScore(BaseModel):
    player_id: int | None = None
    player: str | None = None
    profile_img: str | None = None
    score: int | None = None
    points: int | None = None

    @classmethod
    def from_query_result(cls, id, player, score=0, points=0, profile_img=None):
        return cls(
            player_id=int(id) if id is not None else None,
            player=player,
            profile_img=profile_img,
            score=int(score) if score is not None else None,
            points=int(points) if points is not None else None)


class MatchDateUpdate(BaseModel):
    date: datetime


class MatchPlayerUpdate(BaseModel):
    player_id: int | None = None
    player: str
    player_prev: str


class MatchScoreUpdate(BaseModel):
    player_id: int | None = None
    player: str
    score: int


class MatchBase(BaseModel):
    id: int | None = None
    date: datetime
    format: MatchFormat
    tournaments_id: int | None = None
    next_match: int | None = None
    round: int | None = None

    @classmethod
    def from_query_result(cls, id, date, format, tournaments_id, next_match, round):
        return cls(
            id=id,
            date=date,
            format=format,
            tournaments_id=tournaments_id,
            next_match=next_match,
            round=round)


class Match(BaseModel):
    id: int | None = None
    date: datetime
    format: MatchFormat
    participants: List[PlayerProfile]

    @classmethod
    def from_query_result(cls, id, date, format, participants=None):
        if participants == '' or participants is None:
            participants = []
        else:
            participants = list(PlayerProfile.from_query_result(*row) for row in participants)
        return cls(
            id=id,
            date=date,
            format=format,
            participants=participants)


class MatchResponse(BaseModel):
    id: int
    date: datetime
    format: str
    participants: List[PlayerProfile]
    score: List[MatchScore]

    @classmethod
    def from_query_result(cls, id, date, format, participants=None, score=None):
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
            participants=participants,
            score=score)


class MatchTournamentResponse(BaseModel):
    id: int
    date: datetime
    format: str
    tournament_id: int | None = None
    tournament_title: str | None = None
    score: List[MatchScore]

    @classmethod
    def from_query_result(cls, id, date, format, tournament_id, title, score):
        if score == '' or score is None:
            score = []
        else:
            score = list(MatchScore.from_query_result(*row) for row in score)
        return cls(
            id=id,
            date=date,
            format=str(MatchFormat(format)),
            tournament_id=tournament_id,
            tournament_title=title,
            score=score)


class PaginatedMatch(BaseModel):
    matches: list[MatchTournamentResponse]
    pagination: Pagination
