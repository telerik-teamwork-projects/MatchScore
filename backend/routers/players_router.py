from fastapi import Depends, APIRouter
from mariadb import IntegrityError
from typing import List
from models import players, users
from common import authorization, exceptions, responses
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
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")
    
    return players_service.accept_player_request(request_id)

@router.post("/requests/reject/{request_id}")
def reject_player_request(
    request_id: int,
    current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    return players_service.reject_player_request(request_id)


@router.post("/tournament-request/{tournament_id}")
def send_join_tournament_request_no_player(
    tournament_id: int, 
    player_data: players.PlayerCreate, 
    current_user: users.User = Depends(authorization.get_current_user)
):
    # try:
    player_profile = players_service.get_player_by_user_id(current_user.id)
    if player_profile:
        raise exceptions.BadRequest("User already have a player profile")

    players_service.create_tournament_join_request_no_player(tournament_id, player_data, current_user)
    

    return responses.RequestOK("Join request sent successfully")

    # except IntegrityError:
        # raise exceptions.IntegrityError("Join request already sent")
    # except Exception:
        # raise exceptions.InternalServerError("Sending join request failed")
    
@router.post("/tournament-request/{tournament_id}/existing")
def send_join_tournament_request_with_player(
    tournament_id: int, 
    current_user: users.User = Depends(authorization.get_current_user)
):
    # try:
    player_profile = players_service.get_player_by_user_id(current_user.id)
    if not player_profile:
        raise exceptions.BadRequest("User does not have a player profile")
    
    players_service.create_tournament_join_request_with_player(
        tournament_id, 
        player_profile
    )
    
    return responses.RequestOK("Join request sent successfully")

    # except IntegrityError:
        # raise exceptions.IntegrityError("Join request already sent")
    # except Exception:
        # raise exceptions.InternalServerError("Sending join request failed")
    
