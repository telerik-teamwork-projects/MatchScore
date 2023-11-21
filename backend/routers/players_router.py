from fastapi import APIRouter, Query, Form, File, UploadFile, Depends
from typing import Union
from common.exceptions import NotFound, Unauthorized, BadRequest, InternalServerError
from common.utils import manage_pages
from models.pagination import Pagination
from models.players import PlayerProfileImg, PaginatedPlayers
from models.users import User
from common.authorization import get_current_user
from services import players_service

router = APIRouter()


@router.get('/', response_model=PaginatedPlayers)
def get_players(page: int = Query(default=1)):
    total_players = players_service.count()
    params, (page, total_pages) = manage_pages(page, total_players)
    result = players_service.all(params)

    return PaginatedPlayers(players=list(result),
                            pagination=Pagination(page=page, items_per_page=params[-1], total_pages=total_pages))


@router.get('/{id}/', response_model=PlayerProfileImg)
def get_player_by_id(id: int):
    player = players_service.get_by_id(id)

    if player:
        return player

    raise NotFound(f'Player {id} does not exist')


@router.put('/{id}/update/', response_model=PlayerProfileImg)
def player_update(
    id: int,
    full_name: str = Form(None),
    country: str = Form(None),
    sports_club: str = Form(None),
    profile_img: Union[UploadFile, str] = File(None),
    current_user: User = Depends(get_current_user)
):
    target_player = players_service.get_by_id(id)
    if not target_player:
        raise NotFound(f"Player with id {id} doesn't exist") 
    
    if target_player.user_id != current_user.id:
        raise Unauthorized("You are not authorized")
    
    if full_name and full_name != target_player.full_name:
        if players_service.get_player_by_full_name(full_name):
            raise BadRequest("Player with this full name already exists")
        
    profile_image_path = players_service.handle_profile_image(profile_img) 

    # try:
    return players_service.update(
        target_player,
        full_name,
        country,
        sports_club,
        profile_image_path            
    )
    # except Exception:
        # raise InternalServerError("Updating user failed")