import logging
import random as rand
from datetime import timedelta

from common.exceptions import InternalServerError, NotFound, BadRequest
from models import tournaments, requests, players
from services import players_service
from database.database import insert_query, read_query, get_connection
from models.enums import TournamentStatus
from models.users import User
from models.tournaments import Owner
# from models.enums import Request
from models.tournaments import Owner, TournamentLeagueCreate, TournamentLeagueResponse, DbTournament, \
    TournamentRoundResponse
from mariadb import Error
from mariadb.connections import Connection


def create(
        tournament_data: tournaments.TournamentCreate,
        current_user: User
):
    sql = """
        INSERT INTO tournaments (format, title, description, match_format, rounds, third_place, status, location, 
        start_date, end_date, owner_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    sql_params = (
        tournament_data.format.value,
        tournament_data.title,
        tournament_data.description,
        tournament_data.match_format.value,
        tournament_data.rounds,
        tournament_data.third_place,
        tournament_data.status.value,
        tournament_data.location,
        tournament_data.start_date,
        tournament_data.end_date,
        current_user.id
    )

    created_tournament_id = insert_query(sql, sql_params)
    owner = get_owner_data_by_id(current_user.id)
    response_data = tournaments.Tournament(
        id=created_tournament_id,
        format=tournament_data.format,
        title=tournament_data.title,
        description=tournament_data.description,
        match_format=tournament_data.match_format,
        rounds=tournament_data.rounds,
        third_place=tournament_data.third_place,
        status=tournament_data.status,
        location=tournament_data.location,
        start_date=tournament_data.start_date,
        end_date=tournament_data.end_date,
        owner=owner
    )

    return response_data


def get_all():
    sql = """
            SELECT t.*, u.username, u.profile_img
            FROM tournaments t
            JOIN users u ON t.owner_id = u.id
            ORDER BY t.start_date;
        """
    sql_params = ()

    result = read_query(sql, sql_params)

    tournaments_data = []
    for row in result:
        owner = Owner(id=row[11], username=row[12], profile_img=row[13])
        tournament = tournaments.Tournament(
            id=row[0],
            format=row[1],
            title=row[2],
            description=row[3],
            match_format=row[4],
            rounds=row[5],
            third_place=row[6],
            status=row[7],
            location=row[8],
            start_date=str(row[9]),
            end_date=str(row[10]),
            owner=owner
        )
        tournaments_data.append(tournament)

    return tournaments_data


def get_one(tournament_id):
    sql = """
            SELECT t.*, u.username, u.profile_img
            FROM tournaments t
            JOIN users u ON t.owner_id = u.id
            WHERE t.id = ?
        """

    sql_params = (tournament_id,)

    result = read_query(sql, sql_params)

    if result:
        result = result[0]
        owner = Owner(id=result[11], username=result[12], profile_img=result[13])
        tournament = tournaments.Tournament(
            id=result[0],
            format=result[1],
            title=result[2],
            description=result[3],
            match_format=result[4],
            rounds=result[5],
            third_place=result[6],
            status=result[7],
            location=result[8],
            start_date=str(result[9]),
            end_date=str(result[10]),
            owner=owner
        )

        return tournament


def get_tournament_requests(tournament_id: int):
    sql = """
            SELECT *
            FROM tournament_requests
            WHERE tournament_id = ?
        """
    sql_params = (tournament_id,)

    result = read_query(sql, sql_params)
    
    requests_list = [
        requests.TournamentRequest.from_query_result(*request_tuple) for request_tuple in result
    ]

    return requests_list


def accept_player_to_tournament(request_id: int):
    tournament_request  = get_tournament_request_by_id(request_id)
    if not tournament_request:
        raise NotFound("Tournament requests not found") 


    tournament_id = tournament_request.tournament_id
    player_id = tournament_request.player_id
    user_id = tournament_request.user_id

    if not player_id:
        new_player_data = players.PlayerCreate(
            user_id=user_id,
            full_name=tournament_request.full_name,
            country=tournament_request.country,
            sports_club=tournament_request.sports_club
        )

        player_id = players_service.insert_player(
                                        new_player_data.user_id,
                                        new_player_data.full_name,
                                        new_player_data.country,
                                        new_player_data.sports_club
                                        )

    if is_user_accepted(tournament_id, player_id):
        raise BadRequest("Player already in tournament")
    
    update_tournament_request_status(request_id, "accepted")

    sql = """
        INSERT INTO players_tournaments (tournament_id, player_id)
        VALUES (?, ?)
    """
    sql_params = (tournament_id, player_id)
    insert_query(sql, sql_params)



def get_owner_data_by_id(owner_id):
    sql = """
            SELECT username, profile_img 
            FROM users WHERE id = ?;
        """
    sql_params = (owner_id,)

    result = read_query(sql, sql_params)
    if result:
        user = Owner(
            id=owner_id,
            username=result[0][0],
            profile_img=result[0][1]
        )
        return user


def find(id: int):
    data = read_query('SELECT * FROM tournaments WHERE id = ?', (id,))
    return next((DbTournament.from_query_result(*row) for row in data), None)


def get_tournament_by_id(tournament_id):
    sql = "SELECT * FROM tournaments WHERE id = ?"
    sql_params = (tournament_id,)

    result = read_query(sql, sql_params)

    if result:
        result = result[0]
        tournament = tournaments.TournamentWithoutOwner(
            id=result[0],
            format=result[1],
            title=result[2],
            description=result[3],
            match_format=result[4],
            rounds=result[5],
            third_place=result[6],
            status=result[7],
            location=result[8],
            start_date=str(result[9]),
            end_date=str(result[10]),
        )

        return tournament


def is_user_accepted(tournament_id: int, user_id: int):
    sql = "SELECT * FROM players_tournaments WHERE tournament_id = ? AND player_id = ?"
    sql_params = (tournament_id, user_id)

    return len(read_query(sql, sql_params)) > 0


def create_league(data: TournamentLeagueCreate, user: User):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            rounds = len(data.participants) - 1
            end_date = data.start_date + timedelta(days=rounds - 1)
            cursor.execute('''INSERT INTO tournaments (format, title, description, match_format, rounds,  
                                                        status, location, start_date, end_date, owner_id)
                                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (data.format.value, data.title, data.description, data.match_format.value,
                            rounds, TournamentStatus.CLOSED.value, data.location, data.start_date, end_date, user.id))
            tournament_id = cursor.lastrowid
            cursor.execute('SELECT id, username, profile_img FROM users WHERE id = ?', (user.id,))
            owner = cursor.fetchone()

            participants = []
            for p in data.participants:
                cursor.execute('SELECT id FROM players WHERE full_name = ?', (p.full_name,))
                player = cursor.fetchone()
                if player is None:
                    cursor.execute('INSERT INTO players(full_name) VALUES(?)', (p.full_name,))
                    player_id = cursor.lastrowid
                else:
                    player_id = player[0]
                cursor.execute('INSERT INTO players_tournaments(player_id, tournament_id)VALUES(?,?)',
                               (player_id, tournament_id))
                participants.append(player_id)

            _manage_league_matches(cursor, tournament_id, data, participants)
            conn.commit()
            return TournamentLeagueResponse.from_query_result(tournament_id, data.format.value, data.title,
                                                              data.description, data.match_format.value, rounds,
                                                              data.location, data.start_date, end_date, owner)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def view_league_tournament(tournament: DbTournament):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''SELECT m.round, m.id, p.full_name, pm.score, pm.points
                                FROM players_matches pm, players p, matches m
                                WHERE pm.match_id = m.id AND p.id = pm.player_id AND m.tournaments_id = ?
                                ORDER BY m.round, m.id''', (tournament.id,))
            data = list(cursor)
            rounds = []
            for r in range(1, tournament.rounds + 1):
                matches = []
                for el in data:
                    if el[0] == r:
                        if matches and matches[-1][0] == el[1]:
                            matches[-1][1].append(el[2:])
                        else:
                            matches.append([el[1], [el[2:]]])
                rounds.append([r, matches])
            conn.commit()
            return TournamentRoundResponse.from_query_result(tournament.id, rounds)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def _manage_league_matches(cursor: Connection, id: int, data: TournamentLeagueCreate, participants: list[int]):
    rand.shuffle(participants)
    # tournament rounds
    rounds = len(participants) - 1
    # matches per round
    mpr = (rounds + 1) // 2
    # table of participants
    t = [i + 1 for i in range(len(participants))]
    # generate matches along with their participants and rounds they belong to
    date = data.start_date
    for r in range(rounds):
        for m in range(mpr):
            cursor.execute('INSERT INTO matches(date, format, tournaments_id, round) VALUES(?,?,?,?)',
                           (date, data.match_format.value, id, r + 1))
            match_id = cursor.lastrowid
            cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                           (participants[t[m] - 1], match_id))
            cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                           (participants[t[-1 - m] - 1], match_id))

        t.remove(rounds - r + 1)
        t.insert(1, rounds - r + 1)
        date = date + timedelta(days=1)


def update_tournament_request_status(request_id: int, status: str):
    sql = """
        UPDATE tournament_requests
        SET status = ?
        WHERE id = ?
    """
    sql_params = (status, request_id)
    insert_query(sql, sql_params)


def get_tournament_request_by_id(request_id: int):
    sql = """
        SELECT *
        FROM tournament_requests
        WHERE id = ?;
    """
    sql_params = (request_id,)
    result = read_query(sql, sql_params)
    id, player_id, tournament_id, user_id, full_name, country, sports_club, status, created_at = result[0]
    if result:
        return requests.TournamentRequest.from_query_result(
            id=id,
            player_id=player_id,
            tournament_id=tournament_id,
            user_id=user_id,
            full_name=full_name,
            country=country,
            sports_club=sports_club,
            status=status,
            created_at=created_at
        )
    