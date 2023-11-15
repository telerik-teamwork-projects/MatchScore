from database.database import insert_query, read_query 
from models.players import PlayerCreate, PlayerRequest
from models.users import User
from models.enums import Request
from common.exceptions import Unauthorized, NotFound
from common.responses import RequestCreate, RequestOK


def send_player_request(
    user_id: int, 
    player_data: PlayerCreate
):
    sql = """
        INSERT INTO players_requests (requester_id, full_name, country, sports_club, status)
        VALUES (?, ?, ?, ?, ?);
    """
    sql_params = (
        user_id, 
        player_data.full_name,
        player_data.country,
        player_data.sports_club,
        Request.PENDING.value                
    )

    insert_query(sql, sql_params)
    return RequestCreate("Join request sent successfully")


def get_all_player_requests():
    sql = """
        SELECT id, requester_id, full_name, country, sports_club, status
        FROM players_requests
        ORDER BY id DESC;
    """
    sql_params = ()
    result = read_query(sql, sql_params)
    player_requests = [
        PlayerRequest(
            id=row[0],
            requester_id=row[1],
            full_name=row[2],
            country=row[3],
            sports_club=row[4],
            status=row[5]
        )
        for row in result
    ]

    return player_requests


def accept_player_request(request_id:int):

    player_request = get_player_request_by_id(request_id)
    
    if not player_request:
        raise NotFound("Player request not found")

    update_player_request_status(request_id, Request.ACCEPTED.value)

    player_info = get_player_info_from_request(player_request)

    insert_player(player_request.requester_id, **player_info)

    return RequestOK("User accepted as a player")


def reject_player_request(request_id: int):
    player_request = get_player_request_by_id(request_id)

    if not player_request:
        raise NotFound("Player request not found")
    
    update_player_request_status(request_id, Request.REJECTED.value)
    return RequestOK("User request rejected")



def get_player_request_by_id(request_id: int):
    sql = """
        SELECT id, requester_id, full_name, country, sports_club, status
        FROM players_requests
        WHERE id = ?;
    """
    sql_params = (request_id,)
    result = read_query(sql, sql_params)
    result = result[0]
    if result:
        return PlayerRequest(
            id=result[0],
            requester_id=result[1],
            full_name=result[2],
            country=result[3],
            sports_club=result[4],
            status=result[5]
        )
    

def get_player_info_from_request(player_request: PlayerRequest):
    return {
        "full_name": player_request.full_name,
        "country": player_request.country,
        "sports_club": player_request.sports_club,
    }


def update_player_request_status(request_id: int, status: str) -> None:
    sql = """
        UPDATE players_requests
        SET status = ?
        WHERE id = ?;
    """
    sql_params = (status, request_id)
    insert_query(sql, sql_params)


def insert_player(user_id: int, full_name: str, country: str, sports_club: str) -> int:
    sql = """
        INSERT INTO players (user_id, full_name, country, sports_club)
        VALUES (?, ?, ?, ?);
    """
    sql_params = (user_id, full_name, country, sports_club)
    return insert_query(sql, sql_params)