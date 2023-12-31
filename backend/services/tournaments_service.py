import logging
import math
import random as rand
from datetime import timedelta, datetime
from typing import List, Tuple

from common.exceptions import InternalServerError, NotFound, BadRequest
from models import requests, players
from services import players_service
from database.database import insert_query, read_query, get_connection
from models.enums import TournamentStatus, TournamentFormat, KnockoutRounds
from models.users import User
import models.tournaments as t
from mariadb import Error, Cursor
from services.users_service import get_user_by_id
from emails.send_emails import send_tournament_accept_email_async, send_player_tournament_email_async, \
    send_player_match_email_async


def get_all(params: Tuple):
    offset, limit = params
    sql = """
            SELECT t.*, u.username, u.profile_img
            FROM tournaments t
            JOIN users u ON t.owner_id = u.id
            ORDER BY t.start_date DESC
            LIMIT ? OFFSET ?;
        """
    sql_params = (limit, offset)

    result = read_query(sql, sql_params)
    tournaments_data = []
    for row in result:
        tournament_data = row[0:11]
        owner = t.Owner.from_query_result(*row[11:])
        tournament = t.Tournament.from_query_result(
            *tournament_data,
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
        owner = t.Owner(id=result[11], username=result[12], profile_img=result[13])
        tournament = t.Tournament(
            id=result[0],
            format=result[1],
            title=result[2],
            description=result[3],
            match_format=result[4],
            rounds=result[5],
            third_place=result[6],
            status=result[7],
            location=result[8],
            start_date=str(result[9]) if result[9] else result[9],
            end_date=str(result[10]) if result[10] else result[10],
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


async def accept_player_to_tournament(request_id: int):
    tournament_request = get_tournament_request_by_id(request_id)
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
    if user_id:
        user_data = get_user_by_id(user_id)

        subject = "Tournament Acceptance Notification"
        email_to = user_data.email
        body = {
            "title": "Congratulations! You've been accepted to the tournament.",
            "name": tournament_request.full_name,
            "ctaLink": f"http://localhost:3000/tournaments/{tournament_id}"
        }
        await send_tournament_accept_email_async(subject, email_to, body)


def reject_player_from_tournament(request_id: int):
    tournament_request = get_tournament_request_by_id(request_id)
    if not tournament_request:
        raise NotFound("Tournament not found")

    update_tournament_request_status(request_id, "rejected")


def get_owner_data_by_id(owner_id):
    sql = """
            SELECT username, profile_img 
            FROM users WHERE id = ?;
        """
    sql_params = (owner_id,)

    result = read_query(sql, sql_params)
    if result:
        user = t.Owner(
            id=owner_id,
            username=result[0][0],
            profile_img=result[0][1]
        )
        return user


def find(id: int):
    data = read_query('SELECT * FROM tournaments WHERE id = ?', (id,))
    return next((t.DbTournament.from_query_result(*row) for row in data), None)


def get_tournament_by_id(tournament_id):
    sql = "SELECT * FROM tournaments WHERE id = ?"
    sql_params = (tournament_id,)

    result = read_query(sql, sql_params)

    if result:
        result = result[0]
        tournament = t.TournamentWithoutOwner(
            id=result[0],
            format=result[1],
            title=result[2],
            description=result[3],
            match_format=result[4],
            rounds=result[5],
            third_place=result[6],
            status=result[7],
            location=result[8],
            start_date=str(result[9]) if result[9] else result[9],
            end_date=str(result[10]) if result[10] else result[10],
        )

        return tournament


def is_user_accepted(tournament_id: int, user_id: int):
    sql = "SELECT * FROM players_tournaments WHERE tournament_id = ? AND player_id = ?"
    sql_params = (tournament_id, user_id)

    return len(read_query(sql, sql_params)) > 0


async def create_league(data: t.TournamentLeagueCreate, user: User):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            rounds = len(data.participants) - 1
            end_date = data.start_date + timedelta(days=rounds - 1)
            cursor.execute('''INSERT INTO tournaments (format, title, description, match_format, rounds,  
                                                        status, location, start_date, end_date, owner_id)
                                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (TournamentFormat.LEAGUE.value, data.title, data.description, data.match_format.value,
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
                cursor.execute('INSERT INTO players_tournaments(player_id, tournament_id) VALUES(?,?)',
                               (player_id, tournament_id))
                participants.append(player_id)

            _manage_league_matches(cursor, tournament_id, data, participants, rounds)
            conn.commit()
            await _send_tournament_emails(cursor, tournament_id, tuple(participants))
            return t.TournamentLeagueResponse.from_query_result(tournament_id, TournamentFormat.LEAGUE.value,
                                                                data.title,
                                                                data.description, data.match_format.value, rounds,
                                                                data.location, data.start_date, end_date, owner)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


async def create_knockout(data: t.TournamentKnockoutCreate, user: User):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            if data.status == TournamentStatus.OPEN:
                rounds = 0
                end_date = None
            else:
                rounds = int(math.log(len(data.participants), 2))
                if data.third_place:
                    rounds += 1
                end_date = data.start_date + timedelta(days=rounds - 1)

            cursor.execute('''INSERT INTO tournaments (format, title, description, match_format, rounds, third_place, 
                                                        status, location, start_date, end_date, owner_id)
                                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)''',
                           (TournamentFormat.KNOCKOUT.value, data.title, data.description, data.match_format.value,
                            rounds, data.third_place, data.status.value, data.location, data.start_date,
                            end_date, user.id))
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
                cursor.execute('INSERT INTO players_tournaments(player_id, tournament_id) VALUES(?,?)',
                               (player_id, tournament_id))
                participants.append(player_id)

            await _send_tournament_emails(cursor, tournament_id, tuple(participants))
            if data.status == TournamentStatus.CLOSED:
                await _manage_knockout_matches(cursor, tournament_id, data.start_date, data.match_format.value,
                                               data.third_place, participants, rounds)
            conn.commit()
            return t.TournamentKnockoutResponse.from_query_result(tournament_id, TournamentFormat.KNOCKOUT.value,
                                                                  data.title, data.description, data.match_format.value,
                                                                  rounds, data.third_place, data.location,
                                                                  data.start_date, end_date, owner)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def view_tournament(tournament: t.DbTournament):
    data = read_query('''SELECT m.round, m.id, m.next_match, p.id, p.full_name, pm.score, pm.points, p.profile_img
                                FROM matches m 
                                LEFT JOIN players_matches pm ON pm.match_id = m.id 
                                LEFT JOIN players p ON p.id = pm.player_id
                                WHERE m.tournaments_id = ?
                                ORDER BY m.round, m.id''', (tournament.id,))

    if tournament.format == TournamentFormat.KNOCKOUT.value:
        start = 5 - tournament.rounds
        if not tournament.third_place:
            start -= 1
    rounds = []
    for r in range(1, tournament.rounds + 1):
        matches = []
        for el in data:
            if el[0] == r:
                if matches and matches[-1][0] == el[1]:
                    matches[-1][2].append(el[3:])
                else:
                    if el[3]:
                        matches.append([*el[1:3], [el[3:]]])
                    else:
                        matches.append([*el[1:3], []])
        if tournament.format == TournamentFormat.LEAGUE.value:
            rounds.append([f'Round {r}', matches])
        else:
            phase = KnockoutRounds.from_int(start + r)
            rounds.append([phase, matches])

    return t.TournamentRoundResponse.from_query_result(tournament.id, rounds)


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


def update_date(tournament: t.DbTournament, tournament_date: t.TournamentDateUpdate):
    end_date = tournament_date.date + timedelta(days=tournament.rounds - 1)
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE tournaments SET start_date = ?, end_date = ? WHERE id = ?',
                           (tournament_date.date, end_date, tournament.id))
            result = cursor.rowcount
            if result > 0:
                tournament.start_date = tournament_date.date
                tournament.end_date = end_date
                date = tournament.start_date
                for r in range(tournament.rounds):
                    cursor.execute('UPDATE matches SET date = ? WHERE tournaments_id = ? AND round = ?',
                                   (date, tournament.id, r + 1))
                    date = date + timedelta(days=1)
                conn.commit()
                return tournament
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def check_participants(id: int, players: List[t.TournamentPlayerUpdate], prev=False):
    participants = []
    for item in players:
        if prev:
            sql_params = (item.player_prev, id)
        else:
            sql_params = (item.player, id)
        data = read_query('''SELECT p.id FROM players p, players_tournaments pt
                                    WHERE p.full_name = ?
                                    AND p.id = pt.player_id
                                    AND pt.tournament_id = ?''', sql_params)
        if data:
            item_updated = item.model_copy(update={'player_id': data[0][0]})
            participants.append(item_updated)

    if len(players) == len(participants):
        return participants


async def update_players(tournament: t.DbTournament, players_update: List[t.TournamentPlayerUpdate]):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            # re-create players_tournaments with the updated players
            cursor.execute('SELECT player_id FROM players_tournaments WHERE tournament_id = ?', (tournament.id,))
            tournament_players_ids = [i[0] for i in list(cursor)]
            cursor.execute('DELETE FROM players_tournaments WHERE tournament_id = ?', (tournament.id,))
            participants = []
            for p in players_update:
                tournament_players_ids.remove(p.player_id)
                cursor.execute('SELECT id FROM players WHERE full_name = ?', (p.player,))
                player = cursor.fetchone()
                if player is None:
                    cursor.execute('INSERT INTO players(full_name) VALUES(?)', (p.player,))
                    player_id = cursor.lastrowid
                else:
                    player_id = player[0]
                cursor.execute('INSERT INTO players_tournaments(player_id, tournament_id) VALUES(?,?)',
                               (player_id, tournament.id))
                participants.append(player_id)
            send_mails_to = tuple(participants)
            if tournament_players_ids:
                for i in tournament_players_ids:
                    cursor.execute('INSERT INTO players_tournaments(player_id, tournament_id) VALUES(?,?)',
                                   (i, tournament.id))
                    participants.append(i)
            # re-create players_matches using the corresponding randomisation schema
            cursor.execute('SELECT id FROM matches WHERE tournaments_id = ? ORDER BY round', (tournament.id,))
            tournament_matches_ids = [i[0] for i in list(cursor)]
            cursor.execute(f'DELETE FROM players_matches WHERE match_id in {tuple(tournament_matches_ids)}')
            await _send_tournament_emails(cursor, tournament.id, send_mails_to)
            rand.shuffle(participants)
            rounds = tournament.rounds
            mpr = (rounds + 1) // 2
            if tournament.format == TournamentFormat.LEAGUE.value:
                # table of participants
                t = [i + 1 for i in range(len(participants))]
                for r in range(rounds):
                    for m in range(mpr):
                        idx = mpr * r + m
                        match_id = tournament_matches_ids[idx]
                        cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                                       (participants[t[m] - 1], match_id))
                        cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                                       (participants[t[-1 - m] - 1], match_id))
                    t.remove(rounds - r + 1)
                    t.insert(1, rounds - r + 1)
            else:
                # table of participants
                t = [i for i in participants]
                m_count = int(len(participants) / 2)
                for m in range(m_count):
                    cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                                   (t.pop(), tournament_matches_ids[m]))
                    cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                                   (t.pop(), tournament_matches_ids[m]))
                await _send_knockout_matches_emails(cursor, tournament.id, tuple(participants))
            conn.commit()
            return view_tournament(tournament)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def count():
    data = read_query('SELECT COUNT(*) FROM tournaments')
    return data[0][0]


def view_points(tournament: t.DbTournament):
    id = tournament.id
    date_now = (datetime.utcnow() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    if tournament.start_date is not None and date_now <= tournament.start_date:
        date = (tournament.start_date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        matches_played = '0 AS matches_played'
    else:
        date = date_now
        matches_played = 'COUNT(pm.match_id) AS matches_played'
    data = read_query(f'''SELECT pm.player_id, p.full_name, 
                                {matches_played},
                                COALESCE(w.wins, 0) AS wins, 
                                COALESCE(d.draws, 0) AS draws, 
                                COALESCE(l.losses, 0) AS losses,
                                SUM(pm.score) - sc.score_concede AS score_diff, 
                                SUM(pm.points) AS points
                             FROM players_matches pm
                                LEFT JOIN players p ON p.id = pm.player_id
                                LEFT JOIN
                                    (SELECT pm.player_id, p.full_name, COUNT(pm.player_id) AS wins
                                    FROM players_matches pm, players p
                                    WHERE p.id = pm.player_id AND pm.points = 2
                                      AND pm.match_id IN (SELECT id FROM matches WHERE tournaments_id = ? AND date < ?)
                                    GROUP BY pm.player_id) AS w ON pm.player_id = w.player_id
                                LEFT JOIN
                                    (SELECT pm.player_id, p.full_name, COUNT(pm.player_id) AS draws
                                    FROM players_matches pm, players p
                                    WHERE p.id = pm.player_id AND pm.points = 1
                                      AND pm.match_id IN (SELECT id FROM matches WHERE tournaments_id = ? AND date < ?)
                                    GROUP BY pm.player_id) AS d ON pm.player_id = d.player_id
                                LEFT JOIN
                                    (SELECT pm.player_id, p.full_name, COUNT(pm.player_id) AS losses
                                    FROM players_matches pm, players_matches pm1, players p
                                    WHERE p.id = pm.player_id AND pm.points = 0 
                                      AND pm.match_id = pm1.match_id AND pm1.points = 2
                                      AND pm.match_id IN (SELECT id FROM matches WHERE tournaments_id = ? AND date < ?)
                                    GROUP BY pm.player_id) AS l ON pm.player_id = l.player_id
                                LEFT JOIN
                                    (SELECT pm.player_id, p.full_name, SUM(pm1.score) AS score_concede
                                    FROM players_matches pm, players_matches pm1, players p
                                    WHERE p.id = pm.player_id AND pm.match_id = pm1.match_id 
                                       AND pm.player_id != pm1.player_id
                                      AND pm.match_id IN (SELECT id FROM matches WHERE tournaments_id = ? AND date < ?)
                                    GROUP BY pm.player_id) AS sc ON pm.player_id = sc.player_id
                             WHERE pm.match_id IN (SELECT id FROM matches WHERE tournaments_id = ? AND date < ?)
                             GROUP BY pm.player_id 
                             ORDER BY points DESC, score_diff DESC''',
                      (id, date, id, date, id, date, id, date, id, date))

    return t.TournamentPointsResponse.from_query_result(id, data)


def find_participants(id: int):
    data = read_query('SELECT player_id FROM players_tournaments WHERE tournament_id = ?', (id,))
    return [i[0] for i in data]


async def start_knockout(tournament: t.DbTournament, participants: list[int], user: User):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            rounds = int(math.log(len(participants), 2))
            if tournament.third_place:
                rounds += 1
            end_date = tournament.start_date + timedelta(days=rounds - 1)
            cursor.execute('UPDATE tournaments SET start_date = ?, end_date = ?, status = ?, rounds = ? WHERE id = ?',
                           (tournament.start_date, end_date, tournament.status, rounds, tournament.id))
            cursor.execute('SELECT id, username, profile_img FROM users WHERE id = ?', (user.id,))
            owner = cursor.fetchone()
            await _manage_knockout_matches(cursor, tournament.id, tournament.start_date, tournament.match_format,
                                           tournament.third_place, participants, rounds)
            conn.commit()
            return t.TournamentKnockoutResponse.from_query_result(tournament.id, tournament.format, tournament.title,
                                                                  tournament.description, tournament.match_format,
                                                                  rounds,
                                                                  tournament.third_place, tournament.location,
                                                                  tournament.start_date, end_date, owner)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def view_matches(id: int):
    data = read_query('''SELECT m.id, m.next_match, p.id, p.full_name, pm.score, pm.points, p.profile_img
                                    FROM matches m 
                                    LEFT JOIN players_matches pm ON pm.match_id = m.id 
                                    LEFT JOIN players p ON p.id = pm.player_id
                                    WHERE m.tournaments_id = ?
                                    ORDER BY m.round, m.id''', (id,))

    matches = []
    for el in data:
        if matches and matches[-1][0] == el[0]:
            matches[-1][2].append(el[2:])
        else:
            if el[2]:
                matches.append([*el[:2], [el[2:]]])
            else:
                matches.append([*el[:2], []])

    return t.TournamentMatches.from_query_result(id, matches)


def get_players_by_tournament_id(id: int):
    sql = """SELECT players.*
        FROM players_tournaments
        JOIN players ON players_tournaments.player_id = players.id
        WHERE players_tournaments.tournament_id = ?;
    """
    sql_params = (id,)

    result = read_query(sql, sql_params)

    return [players.PlayerProfileImg.from_query_result(*row) for row in result]


async def _manage_knockout_matches(cursor: Cursor, id: int, start_date: datetime, match_format: str, third_place: bool,
                                   participants: list[int], rounds: int):
    rand.shuffle(participants)
    # table of participants
    t = [i for i in participants]
    matches = []
    # matches per round
    m_count = int(len(participants) / 2)
    # generate matches along with the rounds they belong to, link the participants for the first round
    date = start_date
    for r in range(rounds):
        matches.append([])
        for m in range(m_count):
            cursor.execute('INSERT INTO matches(date, format, tournaments_id, round) VALUES(?,?,?,?)',
                           (date, match_format, id, r + 1))
            match_id = cursor.lastrowid
            matches[r].append(match_id)
            if r == 0:
                cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                               (t.pop(), match_id))
                cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                               (t.pop(), match_id))
        m_count = int(m_count / 2)
        if m_count < 1 and third_place:
            m_count = 1
        date = date + timedelta(days=1)
    # update matches with link to their next match
    m_next = rounds
    if third_place:
        m_next -= 1
    for r in range(m_next - 1):
        i = 0
        for m in range(len(matches[r])):
            if m == 0 or m % 2 == 0:
                cursor.execute('UPDATE matches SET next_match = ? WHERE id = ?',
                               (matches[r + 1][i], matches[r][m]))
                i += 1
            else:
                cursor.execute('UPDATE matches SET next_match = ? WHERE id = ?',
                               (matches[r + 1][i - 1], matches[r][m]))
    # send mails
    await _send_knockout_matches_emails(cursor, id, tuple(participants))


def _manage_league_matches(cursor: Cursor, id: int, data: t.TournamentLeagueCreate,
                           participants: list[int], rounds: int):
    rand.shuffle(participants)
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


async def _send_tournament_emails(cursor: Cursor, id: int, participants: tuple[int]):
    subject = "Tournament Notification"
    if len(participants) > 1:
        cursor.execute(f'''SELECT p.full_name, u.email FROM players p, users u 
                                WHERE p.id IN {participants} AND p.user_id = u.id''')
    else:
        cursor.execute(f'''SELECT p.full_name, u.email FROM players p, users u 
                                        WHERE p.id =? AND p.user_id = u.id''', participants)
    data = list(cursor)
    for full_name, email in data:
        email_to = email
        body = {
            "title": "Congratulations! You've been selected to participate in tournament.",
            "name": full_name,
            "ctaLink": f"http://localhost:3000/tournaments/{id}"
        }
        await send_player_tournament_email_async(subject, email_to, body)


async def _send_knockout_matches_emails(cursor: Cursor, id: int, participants: tuple[int]):
    subject = "Match Notification"
    if len(participants) > 1:
        cursor.execute(f'''SELECT p.full_name, u.email FROM players p, users u 
                                   WHERE p.id IN {participants} AND p.user_id = u.id''')
    else:
        cursor.execute(f'''SELECT p.full_name, u.email FROM players p, users u 
                                WHERE p.id IN {participants} AND p.user_id = u.id''')
    data = list(cursor)
    for full_name, email in data:
        email_to = email
        body = {
            "title": "Congratulations! You've qualified to participate in the next phase of our tournament.",
            "name": full_name,
            "ctaLink": f"http://localhost:3000/tournaments/{id}"
        }
        await send_player_match_email_async(subject, email_to, body)
