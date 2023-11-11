import logging
from typing import List

from common.exceptions import InternalServerError
from models.matches import Match, MatchResponse, MatchBase, MatchScoreUpdate
from database.database import get_connection, read_query, insert_query, update_query
from mariadb import Error


def get_format(id: int):
    data = read_query('SELECT format FROM  tournaments WHERE id = ?', (id,))
    return data[0][0]
