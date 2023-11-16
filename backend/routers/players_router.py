from fastapi import Depends, APIRouter
from typing import List
from models import players, users
from common import authorization, exceptions
from services import players_service

router = APIRouter()

@router.post("/{user_id}/player-request")
def send_player_request(
    user_id: int,
    player_data: players.PlayerCreate,
    current_user: users.User = Depends(authorization.get_current_user)
):
    return players_service.send_player_request(user_id, player_data)


@router.get("/requests", response_model=List[players.PlayerRequest])
def get_player_requests(
    current_user: users.User = Depends(authorization.get_current_user)
):
    if not current_user.role.value == "admin":
        raise exceptions.Unauthorized("You are not authorized")
    
    return players_service.get_all_player_requests()


@router.post("/requests/accept/{request_id}")
def accept_player_request(
    request_id: int,
    current_user: users.User = Depends(authorization.get_current_user)
):
    return players_service.accept_player_request(request_id, current_user)