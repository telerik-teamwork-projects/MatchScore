from fastapi import APIRouter
from typing import List
from models import users, players, tournaments
from services import search_service
from common.exceptions import InternalServerError

router = APIRouter()


@router.get("/users-search/", response_model=List[users.User])
def users_search(search: str):
    try:
        return search_service.get_users(search)
    except Exception:
        raise InternalServerError("Loading users failed")


@router.get("/players-search/", response_model=List[players.PlayerProfileImg])
def players_search(search: str):
    try:
        return search_service.get_players(search)
    except Exception:
        raise InternalServerError("Loading players failed")


@router.get("/tournaments-search/", response_model=List[tournaments.TournamentWithoutOwner])
def tournaments_search(search: str):
    try:
        return search_service.get_tournaments(search)
    except Exception:
        raise InternalServerError("Loading tournaments failed")
