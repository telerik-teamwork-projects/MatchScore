from fastapi import APIRouter, Depends
from typing import List

from common.authorization import get_current_user
from common.exceptions import Unauthorized, InternalServerError, BadRequest, NotFound
from common.utils import is_admin, is_director
from models.enums import TournamentFormat
from models.tournaments import Tournament, TournamentCreate, TournamentLeagueCreate, TournamentLeagueResponse, \
    TournamentRoundResponse
from models.users import User

from services import tournaments_service

router = APIRouter()
MAX_PARTICIPANTS = 16
MIN_PARTICIPANTS = 2


@router.post('/knockout', response_model=Tournament, status_code=201)
def create_tournament(tournament_data: TournamentCreate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized("You are not authorized")
    try:
        return tournaments_service.create(tournament_data, current_user)
    except Exception:
        raise InternalServerError("Creating tournament failed")


@router.get("/", response_model=List[Tournament])
def get_tournaments():
    try:
        return tournaments_service.get_all()
    except Exception:
        raise InternalServerError("Retrieving tournaments failed")


@router.get("/{tournament_id}", response_model=Tournament)
def get_tournament(tournament_id):
    try:
        return tournaments_service.get_one(tournament_id)
    except Exception:
        raise InternalServerError("Retrieving tournament details failed")


@router.post("/{tournament_id}/add/{user_id}")
def add_player(
        tournament_id: int,
        user_id: int,
        current_user: User = Depends(get_current_user)
):
    pass


@router.post('/league', response_model=TournamentLeagueResponse, status_code=201)
def create_league_tournament(tournament: TournamentLeagueCreate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized("User has insufficient privileges")
    if tournament.format != TournamentFormat.LEAGUE.value:
        raise BadRequest("Wrong tournament format!")
    p_count = len({p.full_name for p in tournament.participants})
    if p_count != len(tournament.participants):
        raise BadRequest("Participants should be unique!")
    if p_count % 2 != 0:
        raise BadRequest("Participants should be even number!")
    if p_count > MAX_PARTICIPANTS or p_count < MIN_PARTICIPANTS:
        raise BadRequest(f'Participants must be between {MIN_PARTICIPANTS} and {MAX_PARTICIPANTS}!')

    return tournaments_service.create_league(tournament, current_user)


@router.get('/{id}/rounds', response_model=TournamentRoundResponse)
def view_rounds(id: int):
    tournament = tournaments_service.find(id)
    if tournament is None:
        raise NotFound(f'Tournament {id} does not exist!')
    if tournament.format != TournamentFormat.LEAGUE.value:
        raise BadRequest("Wrong tournament format!")

    return tournaments_service.view_league_tournament(tournament)
