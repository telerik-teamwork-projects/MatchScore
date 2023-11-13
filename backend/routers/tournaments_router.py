from fastapi import APIRouter, Depends
from typing import List
from models import tournaments, users, requests

from common.authorization import get_current_user
from common.exceptions import Unauthorized, InternalServerError, NotFound, BadRequest

from services import tournaments_service, users_service

router = APIRouter()


@router.post('/', response_model=tournaments.Tournament, status_code=201)
def create_tournament(
    tournament_data: tournaments.TournamentCreate,
    current_user: users.User = Depends(get_current_user)
):
    if current_user.role.value not in ("admin", "director"):
        raise Unauthorized("You are not authorized")
    
    try:
        return tournaments_service.create(tournament_data, current_user)
    except Exception:
        raise InternalServerError("Creating tournament failed")
    
    
@router.get("/", response_model=List[tournaments.Tournament])
def get_tournaments():
    try:
        return tournaments_service.get_all()
    except Exception:
        raise InternalServerError("Retrieving tournaments failed")
    

@router.get("/{tournament_id}", response_model=tournaments.Tournament)
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

@router.post("/{tournament_id}/accept/{user_id}")
def accept_user(
    tournament_id: int,
    user_id: int,
    current_user: users.User = Depends(get_current_user)
):
    tournament = tournaments_service.get_one(tournament_id)
    if not tournament:
        raise NotFound("Tournament not found")
    
    user = users_service.get_user_by_id(user_id)
    if not user:
        raise NotFound("User not found")

    if not tournament.owner.id == current_user.id or current_user.role.value != "admin":
        raise Unauthorized("You are not authorized")
    
    if tournaments_service.is_user_accepted(tournament_id, user_id):
        raise BadRequest("User already in tournament")
    
    tournaments_service.accept_user(tournament_id, user_id)