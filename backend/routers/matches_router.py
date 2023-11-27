from datetime import datetime
from typing import List

from fastapi import APIRouter, Query, Depends

from common.authorization import get_current_user
from common.exceptions import Unauthorized, NotFound, BadRequest
from common.utils import is_admin, is_director, manage_pages
from models.enums import TournamentFormat
from models.matches import Match, MatchResponse, MatchScoreUpdate, MatchBase, MatchDateUpdate, MatchPlayerUpdate, \
    MatchTournamentResponse, PaginatedMatch
from models.pagination import Pagination
from models.users import User

from services import matches_service, tournaments_service

router = APIRouter()


@router.post('/', response_model=MatchResponse, status_code=201)
def create_match(match: Match, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')
    p_count = len({p.full_name for p in match.participants})
    if p_count != len(match.participants):
        raise BadRequest("Participants should be unique!")
    if p_count < 2:
        raise BadRequest("Participants must be at least 2!")

    return matches_service.create(match)


@router.put('/{id}/score', response_model=MatchResponse)
def update_score(id: int, match_score: List[MatchScoreUpdate], current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')
    match = matches_service.find(id)
    if match is None:
        raise NotFound(f'Match {id} does not exist')
    if match.date > datetime.utcnow():
        raise BadRequest('The match date is in the future!')
    participants = matches_service.find_participants(id, match_score)
    if participants is None:
        raise NotFound(f'The participants provided do not play in this match')
    negative_scores = [i for i in match_score if i.score < 0]
    if negative_scores:
        raise BadRequest('Match score cannot be negative!')
    if len(match_score) < 2:
        raise BadRequest('Please fill the score for all participants!')
    if match.tournaments_id:
        tournament = tournaments_service.find(match.tournaments_id)
        if tournament.format == TournamentFormat.KNOCKOUT.value:
            if match_score[0].score == match_score[1].score:
                raise BadRequest('There are no draws in knockout tournaments!')
        return matches_service.update_score(match, participants, tournament)

    return matches_service.update_score(match, participants)


@router.put('/{id}/date', response_model=MatchBase)
def update_date(id: int, match_date: MatchDateUpdate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')
    match = matches_service.find(id)
    if match is None:
        raise NotFound(f'Match {id} does not exist')
    if match.tournaments_id is not None:
        raise BadRequest("The date cannot be changed! The match is part of tournament!")
    if match_date.date < datetime.utcnow():
        raise BadRequest('The new match date should be in the future!')

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
        raise BadRequest("The participants cannot be changed! The match is part of tournament!")
    p_count = len({p.player for p in match_players})
    p_prev_count = len({p.player_prev for p in match_players})
    if (p_count != len(match_players)) or (p_prev_count != len(match_players)):
        raise BadRequest("Participants should be unique!")
    participants = matches_service.find_participants(id, match_players)
    if participants is not None:
        raise BadRequest('The participants provided already play in this match!')
    participants_prev = matches_service.find_participants(id, match_players, prev=True)
    if participants_prev is None:
        raise BadRequest('The participants to be updated do not play in this match!')

    return matches_service.update_players(match, participants_prev)


@router.get('/{id}', response_model=MatchTournamentResponse)
def get_match_by_id(id: int):
    match = matches_service.get_by_id(id)

    if match:
        return match

    raise NotFound(f'Match {id} does not exist')


@router.get('/', response_model=PaginatedMatch)
def get_matches(page: int = Query(default=1), from_dt: datetime | None = None):
    total_matches = matches_service.count(from_dt)
    params, (page, total_pages) = manage_pages(page, total_matches, match_limit=True)

    result = matches_service.all(params, from_dt)

    return PaginatedMatch(matches=list(result),
                          pagination=Pagination(page=page, items_per_page=params[-1], total_pages=total_pages))


@router.get('/tournaments/{tournament_id}')
def get_matches_by_tournament_id(tournament_id: int, page: int = Query(default=1)):
    total_matches = matches_service.count_by_tournament(tournament_id)
    params, (page, total_pages) = manage_pages(page, total_matches, match_limit=False, match_tournament_limit=True)

    result = matches_service.get_by_tournament(params, tournament_id)

    return PaginatedMatch(matches=list(result),
                          pagination=Pagination(page=page, items_per_page=params[-1], total_pages=total_pages))
