from datetime import datetime

from pydantic import BaseModel
from typing import Optional, List

from models.enums import TournamentStatus, TournamentFormat, MatchFormat
from models.matches import MatchScore
from models.users import PlayerProfile


class TournamentCreate(BaseModel):
    format: TournamentFormat = TournamentFormat.KNOCKOUT
    title: str
    description: str
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
    description: Optional[str]
    match_format: MatchFormat = MatchFormat.TIME
    rounds: int
    third_place: bool
    status: TournamentStatus = TournamentStatus.OPEN
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    owner: Owner


class TournamentLeagueCreate(BaseModel):
    format: TournamentFormat = TournamentFormat.LEAGUE
    title: str
    description: str | None = None
    match_format: MatchFormat = MatchFormat.TIME
    rounds: int | None = None
    location: str | None = None
    start_date: datetime
    end_date: datetime | None = None
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
    participants: List[MatchScore]

    @classmethod
    def from_query_result(cls, match_id, participants):
        if participants == '' or participants is None:
            participants = []
        else:
            participants = list(MatchScore.from_query_result(*row) for row in participants)
        return cls(
            match_id=match_id,
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
