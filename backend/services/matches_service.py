import logging
from typing import List

from common.exceptions import InternalServerError
from models.matches import Match, MatchResponse, MatchBase, MatchScoreUpdate, MatchDateUpdate, MatchPlayerUpdate
from database.database import get_connection, read_query, insert_query, update_query
from mariadb import Error


def create(match: Match):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO matches(date, format) VALUES(?,?)', (match.date, match.format.value))
            generated_id = cursor.lastrowid
            cursor.execute('SELECT * FROM matches WHERE id = ?', (generated_id,))
            inserted_row = cursor.fetchone()
            participants = []
            score = []
            for p in match.participants:
                cursor.execute('SELECT * FROM players WHERE full_name = ?', (p.full_name,))
                player = cursor.fetchone()
                if player:
                    cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                                   (player[0], generated_id))
                    participants.append(player)
                else:
                    cursor.execute('INSERT INTO players(full_name) VALUES(?)', (p.full_name,))
                    player_id = cursor.lastrowid
                    cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                                   (player_id, generated_id))
                    participants.append((player_id, p.full_name))
                score.append((generated_id, p.full_name, 0, 0))
            conn.commit()
            inserted_row = list(inserted_row)
            inserted_row.extend([participants, score])
            return next((MatchResponse.from_query_result(*row) for row in [inserted_row]), None)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def find(id: int):
    data = read_query('SELECT * FROM matches WHERE id = ?', (id,))
    return next((MatchBase.from_query_result(*row) for row in data), None)


def exists(id: int):
    return any(read_query('SELECT 1 FROM matches WHERE id = ?', (id,)))


def find_match_participants(id: int, match_update: List[MatchPlayerUpdate], prev=False):
    participants = []
    for item in match_update:
        if prev:
            sql_params = (item.player_prev, id)
        else:
            sql_params = (item.player, id)
        data = read_query('''SELECT p.id FROM players p, players_matches pm
                                    WHERE p.full_name = ?
                                    AND p.id = pm.player_id
                                    AND pm.match_id = ?''', sql_params)
        if data:
            item_updated = item.model_copy(update={'player_id': data[0][0]})
            participants.append(item_updated)

    if len(match_update) == len(participants):
        return participants


def update_simple_score(match: MatchBase, participants: List[MatchScoreUpdate], tournament_id: int | None):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            participants_updated = []
            score_updated = []
            for p in participants:
                cursor.execute('''UPDATE players_matches SET score = ? WHERE match_id = ? AND player_id = ?''',
                               (p.score, match.id, p.player_id))
                participants_updated.append((p.player_id, p.player))
                score_updated.append((match.id, p.player, p.score))
            if tournament_id is not None:
                pass
                # manage winner in case of tournament
            conn.commit()
            return MatchResponse.from_query_result(match.id, match.date, match.format, match.tournament_id,
                                                   participants_updated, score_updated)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def update_league_score(match: MatchBase, participants: List[MatchScoreUpdate]):
    pass


def update_date(match: MatchBase, match_date: MatchDateUpdate):
    result = update_query('UPDATE matches SET date = ? WHERE id = ?', (match_date.date, match.id))
    if result > 0:
        match.date = match_date.date
        return match

    raise InternalServerError("Something went wrong")


def update_players(match: MatchBase, players_update: List[MatchPlayerUpdate]):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM players_matches WHERE  match_id = ?', (match.id,))
            data = list(cursor)
            cursor.execute('DELETE FROM players_matches WHERE match_id = ?', (match.id,))
            participants = []
            scores = []
            for p in players_update:
                _, _, score, points = next(row for row in data if row[0] == p.player_id)
                cursor.execute('SELECT * FROM players WHERE full_name = ?', (p.player,))
                player = cursor.fetchone()
                if player:
                    cursor.execute('INSERT INTO players_matches VALUES(?,?,?,?)', (player[0], match.id, score, points))
                    participants.append(player)
                else:
                    cursor.execute('INSERT INTO players(full_name) VALUES(?)', (p.player,))
                    player_id = cursor.lastrowid
                    cursor.execute('INSERT INTO players_matches VALUES(?,?,?,?)', (player_id, match.id, score, points))
                    participants.append((player_id, p.player))
                scores.append((match.id, p.player, score))
            conn.commit()
            return MatchResponse.from_query_result(match.id, match.date, match.format, match.tournament_id,
                                                   participants, scores)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")
