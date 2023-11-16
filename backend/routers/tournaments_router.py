from datetime import datetime
from fastapi import APIRouter, Depends
from typing import List
from models import tournaments, users, requests
from models import users, requests

from common.authorization import get_current_user
from common.exceptions import Unauthorized, InternalServerError, BadRequest, NotFound
from common.utils import is_admin, is_director, is_power_of_two
from common.utils import is_admin, is_director
from common.responses import RequestOK
from models.enums import TournamentFormat
from models.tournaments import Tournament, TournamentCreate, TournamentLeagueCreate, TournamentLeagueResponse, \
    TournamentRoundResponse, TournamentKnockoutResponse, TournamentKnockoutCreate
from models.users import User
from services.players_service import get_player_by_id
from services import tournaments_service, users_service

router = APIRouter()
MAX_PARTICIPANTS = 16
MIN_PARTICIPANTS = 4


@router.post('/', response_model=Tournament, status_code=201)
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


@router.get("/{tournament_id}/requests", response_model=List[requests.TournamentRequest])
def get_tournament_requests(
        tournament_id: int,
):
    if not tournaments_service.get_tournament_by_id(tournament_id):
        raise NotFound("Tournament not found")
    try:
        return tournaments_service.get_tournament_requests(tournament_id)
    except Exception:
        raise InternalServerError("Retrieving requests failed")


@router.post("/requests/accept/{request_id}")
def accept_player_to_tournament(
    request_id: int,
    current_user: users.User = Depends(get_current_user)
):

    if current_user.role.value not in ["admin", "director"]:
        raise Unauthorized("You are not authorized")

    tournaments_service.accept_player_to_tournament(request_id)
    return RequestOK("Player accepted to tournament")


@router.post("/requests/reject/{request_id}")
def reject_player_from_tournament(
    request_id: int,
    current_user: users.User = Depends(get_current_user)
):

    if current_user.role.value not in ["admin", "director"]:
        raise Unauthorized("You are not authorized")

    tournaments_service.reject_player_from_tournament(request_id)
    return RequestOK("Player rejected from entering tournaments")


@router.post('/league', response_model=TournamentLeagueResponse, status_code=201)
def create_league_tournament(tournament: TournamentLeagueCreate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized("User has insufficient privileges")
    p_count = len({p.full_name for p in tournament.participants})
    if p_count != len(tournament.participants):
        raise BadRequest("Participants should be unique!")
    if p_count > MAX_PARTICIPANTS or p_count < MIN_PARTICIPANTS:
        raise BadRequest(f'Participants must be between {MIN_PARTICIPANTS} and {MAX_PARTICIPANTS}!')
    if p_count % 2 != 0:
        raise BadRequest("Participants should be even number!")
    if tournament.date <= datetime.utcnow():
        raise BadRequest("Tournament date should be in the future!")

    return tournaments_service.create_league(tournament, current_user)


@router.post('/knockout', response_model=TournamentKnockoutResponse, status_code=201)
def create_knockout_tournament(tournament: TournamentKnockoutCreate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized("User has insufficient privileges")
    p_count = len({p.full_name for p in tournament.participants})
    if p_count != len(tournament.participants):
        raise BadRequest("Participants should be unique!")
    if p_count > MAX_PARTICIPANTS or p_count < MIN_PARTICIPANTS:
        raise BadRequest(f'Participants must be between {MIN_PARTICIPANTS} and {MAX_PARTICIPANTS}!')
    if not is_power_of_two(p_count):
        raise BadRequest("Number of participants for knockout tournament is not correct!")
    if tournament.date <= datetime.utcnow():
        raise BadRequest("Tournament date should be in the future!")

    return tournaments_service.create_knockout(tournament, current_user)


@router.get('/{id}/rounds', response_model=TournamentRoundResponse)
def view_rounds(id: int):
    tournament = tournaments_service.find(id)
    if tournament is None:
        raise NotFound(f'Tournament {id} does not exist!')

    return tournaments_service.view_tournament(tournament)
