from fastapi import APIRouter, Depends
from typing import List
from models import tournaments, users, requests

from common.authorization import get_current_user
from common.exceptions import Unauthorized, InternalServerError, NotFound

from services import tournaments_service

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
    # try:
    return tournaments_service.get_all()
    # except Exception:
        # raise InternalServerError("Retrieving tournaments failed")
    

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
    # try:
    return tournaments_service.get_tournament_requests(tournament_id)
    # except Exception:
        # raise InternalServerError("Retrieving requests failed")

@router.post("/{tournament_id}/add/{user_id}")
def add_player(
    tournament_id: int,
    user_id: int,
    current_user: users.User = Depends(get_current_user)
):
    pass