from fastapi import APIRouter, Depends

from models import tournaments, users

from common.authorization import get_current_user
from common.exceptions import Unauthorized, InternalServerError

from services import tournaments_service

router = APIRouter()


@router.post('/', response_model=tournaments.Tournament, status_code=201)
def create_tournament(
    tournament_data: tournaments.TournamentCreate,
    current_user: users.User = Depends(get_current_user)
):
    if current_user.role.value not in ("admin", "director"):
        raise Unauthorized("You are not authorized")
    
    # try:

    return tournaments_service.create(tournament_data, current_user)
    # except Exception:
        # raise InternalServerError("Creating tournament failed")