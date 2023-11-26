from datetime import datetime
from fastapi import APIRouter, Depends
from typing import List

from common.authorization import get_current_user
from common.exceptions import Unauthorized, InternalServerError, BadRequest, NotFound
from common.utils import is_admin, is_director, is_power_of_two, manage_pages
from models.enums import TournamentFormat, TournamentStatus
import models.tournaments as t
from models.pagination import Pagination
from models.users import User
from services import tournaments_service

router = APIRouter()
MAX_PARTICIPANTS = 16
MIN_PARTICIPANTS = 4


@router.get("/", response_model=t.TournamentPagination)
def get_tournaments(page: int = 1):
    try:
        tournaments_count = tournaments_service.count()
        params, (page, total_pages) = manage_pages(page, tournaments_count)
        result = tournaments_service.get_all(params)

        return t.TournamentPagination(tournaments=list(result),
                                      pagination=Pagination(page=page, items_per_page=params[-1],
                                                            total_pages=total_pages))
    except Exception:
        raise InternalServerError("Retrieving tournaments failed")


@router.get("/{tournament_id}", response_model=t.Tournament)
def get_tournament(tournament_id):
    try:
        return tournaments_service.get_one(tournament_id)
    except Exception:
        raise InternalServerError("Retrieving tournament details failed")


@router.post('/league', response_model=t.TournamentLeagueResponse, status_code=201)
def create_league_tournament(tournament: t.TournamentLeagueCreate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized("User has insufficient privileges")
    p_count = len({p.full_name for p in tournament.participants})
    if p_count != len(tournament.participants):
        raise BadRequest("Participants should be unique!")
    if p_count > MAX_PARTICIPANTS or p_count < MIN_PARTICIPANTS:
        raise BadRequest(f'Participants must be between {MIN_PARTICIPANTS} and {MAX_PARTICIPANTS}!')
    if p_count % 2 != 0:
        raise BadRequest("Participants should be even number!")
    if tournament.start_date <= datetime.utcnow():
        raise BadRequest("Tournament start date should be in the future!")

    return tournaments_service.create_league(tournament, current_user)


@router.post('/knockout', response_model=t.TournamentKnockoutResponse, status_code=201)
def create_knockout_tournament(tournament: t.TournamentKnockoutCreate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized("User has insufficient privileges")
    p_count = len({p.full_name for p in tournament.participants})
    if p_count != len(tournament.participants):
        raise BadRequest("Participants should be unique!")

    # create tournament open for player join requests
    if tournament.status == TournamentStatus.OPEN and len(tournament.participants) < MAX_PARTICIPANTS:
        return tournaments_service.create_knockout(tournament, current_user)

    if p_count > MAX_PARTICIPANTS or p_count < MIN_PARTICIPANTS:
        raise BadRequest(f'Participants must be between {MIN_PARTICIPANTS} and {MAX_PARTICIPANTS}!')
    if not is_power_of_two(p_count):
        raise BadRequest("Number of participants for knockout tournament is not correct!")
    if tournament.start_date <= datetime.utcnow():
        raise BadRequest("Tournament start date should be in the future!")

    tournament.status = TournamentStatus.CLOSED
    return tournaments_service.create_knockout(tournament, current_user)


@router.get('/{id}/rounds', response_model=t.TournamentRoundResponse)
def view_rounds(id: int):
    tournament = tournaments_service.find(id)
    if tournament is None:
        raise NotFound(f'Tournament {id} does not exist!')

    return tournaments_service.view_tournament(tournament)


@router.get('/{id}/points', response_model=t.TournamentPointsResponse)
def view_points(id: int):
    tournament = tournaments_service.find(id)
    if tournament is None:
        raise NotFound(f'Tournament {id} does not exist!')
    if tournament.format != TournamentFormat.LEAGUE.value:
        raise BadRequest(f'Tournament {id} is not league!')

    return tournaments_service.view_points(id)


@router.get('/{id}/matches', response_model=t.TournamentMatches)
def view_matches(id: int):
    tournament = tournaments_service.find(id)
    if tournament is None:
        raise NotFound(f'Tournament {id} does not exist!')

    return tournaments_service.view_matches(id)


@router.put('/{id}/date', response_model=t.DbTournament)
def update_date(id: int, tournament_date: t.TournamentDateUpdate, current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')
    tournament = tournaments_service.find(id)
    if tournament is None:
        raise NotFound(f'Tournament {id} does not exist!')
    if tournament.start_date <= datetime.utcnow():
        raise BadRequest('The tournament has already started!')
    if tournament_date.date < datetime.utcnow():
        raise BadRequest('The new tournament start date should be in the future!')
    if tournament.status == TournamentStatus.OPEN.value:
        raise BadRequest(f'Tournament status should be {str(TournamentStatus.CLOSED)}')

    if tournament.start_date == tournament_date.date:
        return tournament
    return tournaments_service.update_date(tournament, tournament_date)


@router.put('/{id}/players', response_model=t.TournamentRoundResponse)
def update_players(id: int, players: List[t.TournamentPlayerUpdate], current_user: User = Depends(get_current_user)):
    if not is_admin(current_user) and not is_director(current_user):
        raise Unauthorized('User has insufficient privileges')
    tournament = tournaments_service.find(id)
    if tournament is None:
        raise NotFound(f'Tournament {id} does not exist!')
    if tournament.start_date <= datetime.utcnow():
        raise BadRequest('The tournament has already started!')
    p_count = len({p.player for p in players})
    p_prev_count = len({p.player_prev for p in players})
    if (p_count != len(players)) or (p_prev_count != len(players)):
        raise BadRequest("Participants should be unique!")
    participants = tournaments_service.check_participants(id, players)
    if participants is not None:
        raise BadRequest('The participants provided already play in this tournament!')
    participants_prev = tournaments_service.check_participants(id, players, prev=True)
    if participants_prev is None:
        raise BadRequest('The participants to be updated do not play in this match!')
    if tournament.status == TournamentStatus.OPEN.value:
        raise BadRequest(f'Tournament status should be {str(TournamentStatus.CLOSED)}')

    return tournaments_service.update_players(tournament, participants_prev)


@router.put('/{id}/knockout_start', response_model=t.TournamentKnockoutResponse)
def start_knockout_tournament(id: int, tournament_date: t.TournamentDateUpdate, user: User = Depends(get_current_user)):
    if not is_admin(user) and not is_director(user):
        raise Unauthorized("User has insufficient privileges")
    tournament = tournaments_service.find(id)
    if tournament is None:
        raise NotFound(f'Tournament {id} does not exist!')
    if tournament.status == TournamentStatus.CLOSED.value:
        raise BadRequest('The tournament has already started!')
    participants = tournaments_service.find_participants(id)
    p_count = len(participants)
    if p_count > MAX_PARTICIPANTS or p_count < MIN_PARTICIPANTS:
        raise BadRequest(f'Participants must be between {MIN_PARTICIPANTS} and {MAX_PARTICIPANTS}!')
    if not is_power_of_two(p_count):
        raise BadRequest("Number of participants for knockout tournament is not correct!")
    if tournament_date.date <= datetime.utcnow():
        raise BadRequest("Tournament start date should be in the future!")

    tournament.status = TournamentStatus.CLOSED.value
    tournament.start_date = tournament_date.date
    return tournaments_service.start_knockout(tournament, participants, user)
