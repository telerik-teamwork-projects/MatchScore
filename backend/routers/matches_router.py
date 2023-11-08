from fastapi import APIRouter
from common import exceptions
from common.authorization import get_current_user
from common.exceptions import Unauthorized
from common.utils import is_admin, is_director
from models.matches import Match, MatchResponse
from models.users import User
from fastapi import Depends

from services import matches_service

router = APIRouter()


@router.post('/', response_model=MatchResponse, status_code=201)
def create_match(match: Match, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')

    return matches_service.create(match)
