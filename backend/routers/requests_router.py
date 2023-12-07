from fastapi import APIRouter, Depends
from typing import List
from models import users, requests, players, tournaments
from common import authorization, responses, exceptions
from services import requests_service, players_service, tournaments_service

router = APIRouter()


@router.post("/director-requests/")
def send_director_request(
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value == "admin":
        raise exceptions.BadRequest("Admins cannot send a director request")

    if current_user.role.value == "director":
        raise exceptions.BadRequest("User is already a director")

    requests_service.send_director_request(current_user)
    return responses.RequestOK("Successfully sent a director request")


@router.get("/director-requests/", response_model=List[requests.DirectorRequest])
def get_director_requests(
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    return requests_service.get_director_requests()


@router.post("/director-requests/accept/{request_id}/")
async def accept_director_request(
        request_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    await requests_service.accept_director_request(request_id)
    return responses.RequestOK("Director request accepted")


@router.post("/director-requests/reject/{request_id}/")
def reject_director_request(
        request_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    requests_service.reject_director_request(request_id)
    return responses.RequestOK("Director request rejected")


@router.post("/link-player-requests/")
def send_link_to_player_request(
        user_data: users.LinkToPlayerCreate,
        current_user: users.User = Depends(authorization.get_current_user)
):
    requests_service.send_link_to_player_request(current_user, user_data.full_name)
    return responses.RequestOK("Link to player request sent successfully")


@router.get("/link-player-requests/")
def get_link_requests(
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    return requests_service.get_link_requests()


@router.post("/link-player-requests/accept/{request_id}/")
async def accept_link_player_request(
        request_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    await requests_service.accept_link_player_request(request_id, current_user)
    return responses.RequestOK("Link player request accepted")


@router.post("/link-player-requests/reject/{request_id}/")
def reject_link_player_request(
        request_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    requests_service.reject_link_player_request(request_id)
    return responses.RequestOK("Link player request rejected")


@router.post("/player-request/{user_id}/")
def send_player_request(
        user_id: int,
        player_data: players.PlayerCreate,
        current_user: users.User = Depends(authorization.get_current_user)
):
    return players_service.send_player_request(user_id, player_data)


@router.get("/player-requests/", response_model=List[players.PlayerRequest])
def get_player_requests(
        current_user: users.User = Depends(authorization.get_current_user)
):
    if not current_user.role.value == "admin":
        raise exceptions.Unauthorized("You are not authorized")

    return players_service.get_all_player_requests()


@router.post("/player-requests/accept/{request_id}/")
async def accept_player_request(
        request_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    await players_service.accept_player_request(request_id)
    return responses.RequestOK("Player request accepted")


@router.post("/player-requests/reject/{request_id}/")
def reject_player_request(
        request_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value != "admin":
        raise exceptions.Unauthorized("You are not authorized")

    players_service.reject_player_request(request_id)
    return responses.RequestOK("Player request rejected")


@router.post("/tournament-requests/{tournament_id}/")
def send_tournament_request_no_player(
        tournament_id: int,
        player_data: players.PlayerCreate,
        current_user: users.User = Depends(authorization.get_current_user)
):
    player_profile = players_service.get_player_by_user_id(current_user.id)
    if player_profile:
        raise exceptions.BadRequest("User already have a player profile")

    try:
        players_service.create_tournament_join_request_no_player(tournament_id, player_data, current_user)
        return responses.RequestOK("Tournament request sent successfully")

    except Exception:
        raise exceptions.InternalServerError("Sending tournament request failed")


@router.post("/tournament-requests/{tournament_id}/existing/")
def send_tournament_request_with_player(
        tournament_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    player_profile = players_service.get_player_by_user_id(current_user.id)
    if not player_profile:
        raise exceptions.BadRequest("User does not have a player profile")

    try:
        players_service.create_tournament_join_request_with_player(
            tournament_id,
            player_profile
        )
        return responses.RequestOK("Tournament request sent successfully")

    except Exception:
        raise exceptions.InternalServerError("Sending tournament request failed")


@router.get("/tournament-requests/{tournament_id}/", response_model=List[requests.TournamentRequest])
def get_tournament_requests(tournament_id: int):
    if not tournaments_service.get_tournament_by_id(tournament_id):
        raise exceptions.NotFound("Tournament not found")
    try:
        return tournaments_service.get_tournament_requests(tournament_id)
    except Exception:
        raise exceptions.InternalServerError("Retrieving requests failed")


@router.post("/tournament-requests/accept/{request_id}/")
async def accept_tournament_request(
        request_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value not in ["admin", "director"]:
        raise exceptions.Unauthorized("You are not authorized")

    await tournaments_service.accept_player_to_tournament(request_id)
    return responses.RequestOK("Player accepted in tournament")


@router.post("/tournament-requests/reject/{request_id}/")
def reject_tournament_requets(
        request_id: int,
        current_user: users.User = Depends(authorization.get_current_user)
):
    if current_user.role.value not in ["admin", "director"]:
        raise exceptions.Unauthorized("You are not authorized")

    tournaments_service.reject_player_from_tournament(request_id)
    return responses.RequestOK("Player rejected from entering tournaments")
