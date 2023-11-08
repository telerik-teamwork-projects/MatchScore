import logging

from common.exceptions import InternalServerError
from models.matches import Match, MatchResponse
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
            conn.commit()
            inserted_row = list(inserted_row)
            inserted_row.append(participants)
            return next((MatchResponse.from_query_result(*row) for row in [inserted_row]), None)
        except Error as err:
            conn.rollback()
            logging.exception(err.msg)
            raise InternalServerError("Something went wrong")
