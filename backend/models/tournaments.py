from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

from models.enums import TournamentStatus, TournamentFormat, MatchFormat, Request
from models.matches import MatchScore
from models.players import PlayerProfile
from models.pagination import Pagination


class TournamentCreate(BaseModel):
    format: TournamentFormat = TournamentFormat.KNOCKOUT
    title: str
    description: Optional[str] = None
    match_format: MatchFormat = MatchFormat.TIME
    rounds: int | None = None
    third_place: bool
    status: TournamentStatus = TournamentStatus.OPEN
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    owner_id: int | None = None


class TournamentUpdate(BaseModel):
    format: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
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
    profile_img: str | None = None

    @classmethod
    def from_query_result(cls, id, username, profile_img):
        return cls(
            id=id,
            username=username,
            profile_img=profile_img)


class Tournament(BaseModel):
    id: int
    format: TournamentFormat = TournamentFormat.KNOCKOUT
    title: str
    description: Optional[str] = None
    match_format: MatchFormat = MatchFormat.TIME
    rounds: int
    third_place: bool
    status: TournamentStatus = TournamentStatus.OPEN
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner: Owner

    @classmethod
    def from_query_result(cls, id, format, title, description, match_format, rounds, third_place, status, location,
                          start_date, end_date, owner):
        return cls(
            id=id,
            format=format,
            title=title,
            description=description,
            match_format=match_format,
            rounds=rounds,
            third_place=third_place,
            status=status,
            location=location,
            start_date=start_date,
            end_date=end_date,
            owner=owner
        )


class TournamentRequestCreate(BaseModel):
    player_id: int
    tournament_id: int
    full_name: str
    country: str
    sports_club: str
    status: Request = Request.PENDING
    created_at: str


class TournamentRequest(TournamentRequestCreate):
    id: int


class TournamentWithoutOwner(BaseModel):
    id: int
    format: TournamentFormat = TournamentFormat.KNOCKOUT
    title: str
    description: Optional[str] = None
    match_format: MatchFormat = MatchFormat.TIME
    rounds: int
    third_place: bool
    status: TournamentStatus = TournamentStatus.OPEN
    location: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner_id: Optional[int] = None

    @classmethod
    def from_query_result(cls, id, format, title, description, match_format, rounds, third_place, status, location,
                          start_date, end_date, owner_id):
        return cls(
            id=id,
            format=format,
            title=title,
            description=description,
            match_format=match_format,
            rounds=rounds,
            third_place=third_place,
            status=status,
            location=location,
            start_date=start_date,
            end_date=end_date,
            owner_id=owner_id
        )


class TournamentLeagueCreate(BaseModel):
    title: str
    description: str | None = None
    match_format: MatchFormat = MatchFormat.TIME
    location: str | None = None
    start_date: datetime
    participants: List[PlayerProfile]


class TournamentLeagueResponse(BaseModel):
    id: int
    format: str
    title: str
    description: str | None = None
    match_format: str
    rounds: int
    location: str | None = None
    start_date: datetime
    end_date: datetime
    owner: Owner

    @classmethod
    def from_query_result(cls, id, format, title, description, match_format, rounds, location, start_date,
                          end_date, owner):
        owner = Owner.from_query_result(*owner)
        return cls(id=id,
                   format=str(TournamentFormat(format)),
                   title=title,
                   description=description,
                   match_format=str(MatchFormat(match_format)),
                   rounds=rounds,
                   location=location,
                   start_date=start_date,
                   end_date=end_date,
                   owner=owner)


class TournamentMatch(BaseModel):
    match_id: int
    next_match: int | None = None
    participants: List[MatchScore]

    @classmethod
    def from_query_result(cls, match_id, next_match, participants):
        if participants == '' or participants is None:
            participants = []
        else:
            participants = list(MatchScore.from_query_result(*row) for row in participants)
        return cls(
            match_id=match_id,
            next_match=next_match,
            participants=participants)


class TournamentRound(BaseModel):
    round: int
    matches: List[TournamentMatch]

    @classmethod
    def from_query_result(cls, round, matches):
        if matches == '' or matches is None:
            matches = []
        else:
            matches = list(TournamentMatch.from_query_result(*row) for row in matches)
        return cls(
            round=round,
            matches=matches)


class TournamentRoundResponse(BaseModel):
    id: int
    rounds: List[TournamentRound]

    @classmethod
    def from_query_result(cls, id, rounds):
        if rounds == '' or rounds is None:
            rounds = []
        else:
            rounds = list(TournamentRound.from_query_result(*row) for row in rounds)
        return cls(
            id=id,
            rounds=rounds)


class DbTournament(BaseModel):
    id: int
    format: str
    title: str
    description: str | None = None
    match_format: str
    rounds: int
    third_place: bool
    status: str
    location: str | None = None
    start_date: datetime
    end_date: datetime
    owner_id: int

    @classmethod
    def from_query_result(cls, id, format, title, description, match_format, rounds, third_place, status, location,
                          start_date, end_date, owner_id):
        return cls(id=id,
                   format=format,
                   title=title,
                   description=description,
                   match_format=match_format,
                   rounds=rounds,
                   third_place=third_place,
                   status=status,
                   location=location,
                   start_date=start_date,
                   end_date=end_date,
                   owner_id=owner_id)


class TournamentKnockoutCreate(BaseModel):
    title: str
    description: str | None = None
    match_format: MatchFormat = MatchFormat.TIME
    third_place: bool
    location: str | None = None
    start_date: datetime
    participants: List[PlayerProfile]


class TournamentKnockoutResponse(BaseModel):
    id: int
    format: str
    title: str
    description: str | None = None
    match_format: str
    rounds: int
    third_place: bool
    location: str | None = None
    start_date: datetime
    end_date: datetime
    owner: Owner

    @classmethod
    def from_query_result(cls, id, format, title, description, match_format, rounds, third_place, location, start_date,
                          end_date, owner):
        owner = Owner.from_query_result(*owner)
        return cls(id=id,
                   format=str(TournamentFormat(format)),
                   title=title,
                   description=description,
                   match_format=str(MatchFormat(match_format)),
                   rounds=rounds,
                   third_place=third_place,
                   location=location,
                   start_date=start_date,
                   end_date=end_date,
                   owner=owner)


class TournamentDateUpdate(BaseModel):
    date: datetime


class TournamentPlayerUpdate(BaseModel):
    player_id: int | None = None
    player: str
    player_prev: str


class TournamentPagination(BaseModel):
    tournaments: List[Tournament]
    pagination: Pagination


class TournamentScore(BaseModel):
    score: int

class TournamentPlayerPoints(BaseModel):
    player_id: int
    full_name: str
    matches_played: int
    wins: int
    draws: int
    losses: int
    score_diff: int
    points: int

    @classmethod
    def from_query_result(cls, player_id, full_name, matches_played, wins, draws, losses, score_diff, points):
        return cls(player_id=player_id,
                   full_name=full_name,
                   matches_played=matches_played,
                   wins=wins,
                   draws=draws,
                   losses=losses,
                   score_diff=score_diff,
                   points=points)


class TournamentPointsResponse(BaseModel):
    id: int
    players: List[TournamentPlayerPoints]

    @classmethod
    def from_query_result(cls, id, players):
        if players == '' or players is None:
            players = []
        else:
            players = list(TournamentPlayerPoints.from_query_result(*row) for row in players)
        return cls(
            id=id,
            players=players)
