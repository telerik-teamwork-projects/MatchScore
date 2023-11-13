from fastapi import APIRouter, Depends
from typing import List

from common.authorization import get_current_user
from common.exceptions import Unauthorized, InternalServerError
from common.utils import is_admin, is_director
from models.tournaments import Tournament, TournamentCreate, TournamentLeagueCreate, TournamentLeagueResponse
from models.users import User

from services import tournaments_service

router = APIRouter()


@router.post('/knockout', response_model=Tournament, status_code=201)
def create_tournament(tournament_data: TournamentCreate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized("You are not authorized")

    try:
        return tournaments_service.create(tournament_data, current_user)
    except Exception:
        raise InternalServerError("Creating tournament failed")


@router.post('/league', response_model=TournamentLeagueResponse, status_code=201)
def create_league_tournament(tournament: TournamentLeagueCreate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized("User has insufficient privileges")
    # add checks for player uniqueness and even count

    return tournaments_service.create_league(tournament, current_user)


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
