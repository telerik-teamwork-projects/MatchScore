import logging
from typing import List

from common.exceptions import InternalServerError
from models.matches import Match, MatchResponse, MatchBase, MatchScoreUpdate, MatchDateUpdate, MatchPlayerUpdate
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
                cursor.execute('SELECT * FROM players WHERE full_name = ?', (p.full_name,))
                player = cursor.fetchone()
                if player is None:
                    cursor.execute('INSERT INTO players(full_name) VALUES(?)', (p.full_name,))
                    player_id = cursor.lastrowid
                else:
                    player_id = player[0]
                cursor.execute('INSERT INTO players_matches(player_id, match_id) VALUES(?,?)',
                               (player_id, generated_id))
                participants.append((player_id, p.full_name))
                score.append((p.full_name, 0, 0))
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


def find_match_participants(id: int, match_update: List[MatchPlayerUpdate] | List[MatchScoreUpdate], prev=False):
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
            cursor.execute('''SELECT pm.player_id, pm.score, pm.points, p.full_name 
                                    FROM players_matches pm, players p 
                                    WHERE pm.match_id = ? AND p.id = pm.player_id 
                                    ORDER BY score DESC''', (match.id,))
            data = list(cursor)
            if len(data) == 2:
                if data[0][1] == data[1][1]:
                    cursor.execute('''UPDATE players_matches SET points = 1 WHERE match_id = ?''', (match.id,))
                    score_updated.extend([(data[0][3], data[0][1], 1), (data[1][3], data[0][1], 1)])
                else:
                    cursor.execute('''UPDATE players_matches SET points = 2 WHERE match_id = ? AND player_id = ?''',
                                   (match.id, data[0][0]))
                    cursor.execute('''UPDATE players_matches SET points = 0 WHERE match_id = ? AND player_id = ?''',
                                   (match.id, data[1][0]))
                    score_updated.extend([(data[0][3], data[0][1], 2), (data[1][3], data[1][1], 0)])
                participants_updated.extend([(data[0][0], data[0][3]), (data[1][0], data[1][3])])
            elif len(data) > 2:
                if data[0][1] == data[1][1] == data[2][1]:
                    cursor.execute('''UPDATE players_matches SET points = 1 WHERE match_id = ? AND player_id in ?''',
                                   (match.id, (data[0][0], data[1][0], data[2][0])))
                elif data[0][1] == data[1][1]:
                    cursor.execute('''UPDATE players_matches SET points = 3 WHERE match_id = ? AND player_id in ?''',
                                   (match.id, (data[0][0], data[1][0])))
                    cursor.execute('''UPDATE players_matches SET points = 1 WHERE match_id = ? AND player_id = ?''',
                                   (match.id, data[2][0]))
                elif data[1][1] == data[2][1]:
                    cursor.execute('''UPDATE players_matches SET points = 3 WHERE match_id = ? AND player_id = ?''',
                                   (match.id, data[0][0]))
                    cursor.execute('''UPDATE players_matches SET points = 2 WHERE match_id = ? AND player_id in ?''',
                                   (match.id, (data[1][0], data[2][0])))
                cursor.execute('''UPDATE players_matches SET points = 0 WHERE match_id = ? AND player_id not in ?''',
                               (match.id, (data[0][0], data[1][0], data[2][0])))
                for p in data:
                    participants_updated.append([p[0], p[3]])
                    score_updated.append([p[3], p[1], p[2]])
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
            cursor.execute('SELECT * FROM players_matches WHERE  match_id = ?', (match.id,))
            data = list(cursor)
            cursor.execute('DELETE FROM players_matches WHERE match_id = ?', (match.id,))
            participants = []
            scores = []
            for p in players_update:
                _, _, score, points = next(row for row in data if row[0] == p.player_id)
                cursor.execute('SELECT * FROM players WHERE full_name = ?', (p.player,))
                player = cursor.fetchone()
                if player is None:
                    cursor.execute('INSERT INTO players(full_name) VALUES(?)', (p.player,))
                    player_id = cursor.lastrowid
                else:
                    player_id = player[0]
                cursor.execute('INSERT INTO players_matches VALUES(?,?,?,?)', (player_id, match.id, score, points))
                participants.append((player_id, p.player))
                scores.append((p.player, score, points))
            conn.commit()
            return MatchResponse.from_query_result(match.id, match.date, match.format, participants, scores)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")
