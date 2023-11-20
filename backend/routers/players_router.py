from fastapi import APIRouter, Query

from common.exceptions import NotFound
from common.utils import manage_pages
from models.pagination import Pagination
from models.players import PlayerProfileImg, PaginatedPlayers
from services import players_service

router = APIRouter()


@router.get('/', response_model=PaginatedPlayers)
def get_players(page: int = Query(default=1)):
    total_players = players_service.count()
    params, (page, total_pages) = manage_pages(page, total_players)

    result = players_service.all(params)

    return PaginatedPlayers(players=list(result),
                            pagination=Pagination(page=page, items_per_page=params[-1], total_pages=total_pages))


@router.get('/{id}', response_model=PlayerProfileImg)
def get_player_by_id(id: int):
    player = players_service.get_by_id(id)

    if player:
        return player

    raise NotFound(f'Player {id} does not exist')
