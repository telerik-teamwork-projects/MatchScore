import logging
from typing import List

from common.exceptions import InternalServerError
from models.matches import Match, MatchResponse, MatchBase, MatchScoreUpdate, MatchDateUpdate, MatchPlayerUpdate, \
    MatchTournamentResponse
from database.database import get_connection, read_query, update_query
from mariadb import Error


def create(match: Match):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO matches(date, format) VALUES(?,?)', (match.date, match.format.value))
            generated_id = cursor.lastrowid
            cursor.execute('SELECT id, date, format FROM matches WHERE id = ?', (generated_id,))
            inserted_row = cursor.fetchone()
            participants = []
            score = []
            for p in match.participants:
                cursor.execute('SELECT id FROM players WHERE full_name = ?', (p.full_name,))
                player = cursor.fetchone()
                if player is None:
                    cursor.execute('INSERT INTO players(full_name) VALUES(?)', (p.full_name,))
                    player_id = cursor.lastrowid
                else:
                    player_id = player[0]
                cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                               (player_id, generated_id))
                participants.append((player_id, p.full_name))
                score.append((player_id, p.full_name, 0, 0))
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


def find_participants(id: int, match_update: List[MatchPlayerUpdate] | List[MatchScoreUpdate], prev=False):
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


def update_score(match: MatchBase, participants: List[MatchScoreUpdate]):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            participants_updated = []
            score_updated = []
            # manage score
            for p in participants:
                cursor.execute('''UPDATE players_matches SET score = ? WHERE match_id = ? AND player_id = ?''',
                               (p.score, match.id, p.player_id))
            # manage points
            cursor.execute('''SELECT pm.player_id, p.full_name, pm.score, pm.points  
                                    FROM players_matches pm, players p 
                                    WHERE pm.match_id = ? AND p.id = pm.player_id 
                                    ORDER BY score DESC''', (match.id,))
            data = list(cursor)
            if len(data) == 2:
                if data[0][2] == data[1][2]:
                    cursor.execute('''UPDATE players_matches SET points = 1 WHERE match_id = ?''', (match.id,))
                    score_updated.extend([(*data[0][:3], 1), (*data[1][:3], 1)])
                else:
                    cursor.execute('''UPDATE players_matches SET points = 2 WHERE match_id = ? AND player_id = ?''',
                                   (match.id, data[0][0]))
                    cursor.execute('''UPDATE players_matches SET points = 0 WHERE match_id = ? AND player_id = ?''',
                                   (match.id, data[1][0]))
                    score_updated.extend([(*data[0][:3], 2), (*data[1][:3], 0)])
                participants_updated.extend([[*data[0][:2]], [*data[1][:2]]])
            elif len(data) > 2:
                # give points only for the first three players
                if data[0][2] == data[1][2] == data[2][2]:
                    cursor.execute(f'''UPDATE players_matches SET points = 1 
                                       WHERE match_id = ? 
                                       AND player_id in {(data[0][0], data[1][0], data[2][0])}''', (match.id,))
                elif data[0][2] == data[1][2]:
                    cursor.execute(f'''UPDATE players_matches SET points = 3 
                                       WHERE match_id = ? AND player_id in {(data[0][0], data[1][0])}''', (match.id,))
                    cursor.execute('UPDATE players_matches SET points = 1 WHERE match_id = ? AND player_id = ?',
                                   (match.id, data[2][0]))
                elif data[1][2] == data[2][2]:
                    cursor.execute('UPDATE players_matches SET points = 3 WHERE match_id = ? AND player_id = ?',
                                   (match.id, data[0][0]))
                    cursor.execute(f'''UPDATE players_matches SET points = 2 
                                       WHERE match_id = ? AND player_id in {(data[1][0], data[2][0])}''', (match.id,))
                cursor.execute(f'''UPDATE players_matches SET points = 0 
                                   WHERE match_id = ? 
                                   AND player_id not in {(data[0][0], data[1][0], data[2][0])}''', (match.id,))
                for p in data:
                    participants_updated.append([*p[0:2]])
                    score_updated.append([*p])
            conn.commit()
            return MatchResponse.from_query_result(match.id, match.date, match.format, participants_updated,
                                                   score_updated)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


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
            cursor.execute('SELECT * FROM players_matches WHERE match_id = ?', (match.id,))
            data = list(cursor)
            cursor.execute('DELETE FROM players_matches WHERE match_id = ?', (match.id,))
            participants = []
            scores = []
            for p in players_update:
                id, match_id, score, points = next(row for row in data if row[0] == p.player_id)
                data.remove((id, match_id, score, points))
                cursor.execute('SELECT * FROM players WHERE full_name = ?', (p.player,))
                player = cursor.fetchone()
                if player is None:
                    cursor.execute('INSERT INTO players(full_name) VALUES(?)', (p.player,))
                    player_id = cursor.lastrowid
                else:
                    player_id = player[0]
                cursor.execute('INSERT INTO players_matches VALUES(?,?,?,?)', (player_id, match.id, score, points))
                participants.append((player_id, p.player))
                scores.append((player_id, p.player, score, points))
            if data:
                for p in data:
                    cursor.execute('INSERT INTO players_matches VALUES(?,?,?,?)', (*p,))
                    cursor.execute('SELECT full_name FROM players WHERE id = ?', (p[0],))
                    name = cursor.fetchone()
                    participants.append((p[0], *name))
                    scores.append((p[0], *name, *p[2:]))
            conn.commit()
            return MatchResponse.from_query_result(match.id, match.date, match.format, participants, scores)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")


def get_by_id(id: int):
    data = read_query('''SELECT m.id, m.date, m.format, t.id, t.title, p.id, p.full_name, pm.score, pm.points
                                FROM matches m 
                                LEFT JOIN players_matches pm ON pm.match_id = m.id 
                                LEFT JOIN players p ON p.id = pm.player_id
                                LEFT JOIN tournaments t ON m.tournaments_id = t.id
                                WHERE m.id = ?''', (id,))
    if data:
        scores = []
        for el in data:
            if el[5]:
                scores.append(el[5:])
        return MatchTournamentResponse.from_query_result(*data[0][:5], scores)
