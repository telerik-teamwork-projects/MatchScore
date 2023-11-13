from datetime import datetime
from typing import List

from fastapi import APIRouter

from common.authorization import get_current_user
from common.exceptions import Unauthorized, NotFound, Forbidden
from common.utils import is_admin, is_director
from models.matches import Match, MatchResponse, MatchScoreUpdate, MatchBase, MatchDateUpdate, MatchPlayerUpdate
from models.users import User
from fastapi import Depends

from services import matches_service

router = APIRouter()


@router.post('/', response_model=MatchResponse, status_code=201)
def create_match(match: Match, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')

    return matches_service.create(match)


@router.put('/{id}/score', response_model=MatchResponse)
def update_score(id: int, match_score: List[MatchScoreUpdate], current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')
    match = matches_service.find(id)
    if match is None:
        raise NotFound(f'Match {id} does not exist')
    if match.date > datetime.utcnow():
        raise Forbidden('The match date is in the future!')
    participants = matches_service.find_match_participants(id, match_score)
    if participants is None:
        raise NotFound(f'The participants provided do not play in this match')

    return matches_service.update_score(match, participants)


@router.put('/{id}/date', response_model=MatchBase)
def update_date(id: int, match_date: MatchDateUpdate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')
    match = matches_service.find(id)
    if match is None:
        raise NotFound(f'Match {id} does not exist')
    if match_date.date < datetime.utcnow() and not is_admin(current_user):
        raise Forbidden('The new match date should be in the future!')

    if match.date == match_date.date:
        return match
    return matches_service.update_date(match, match_date)


@router.put('/{id}/players', response_model=MatchResponse)
def update_players(id: int, match_players: List[MatchPlayerUpdate], current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')
    match = matches_service.find(id)
    if match is None:
        raise NotFound(f'Match {id} does not exist')
    if match.tournaments_id is not None:
        raise Forbidden("The participants cannot be changed! The match is part of tournament!")
    participants = matches_service.find_match_participants(id, match_players)
    if participants is not None:
        raise Forbidden('The participants provided already play in this match!')
    participants_prev = matches_service.find_match_participants(id, match_players, prev=True)
    if participants_prev is None:
        raise Forbidden('The participants to be updated do not play in this match!')

    return matches_service.update_players(match, participants_prev)
