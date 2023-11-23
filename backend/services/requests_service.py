from database.database import read_query, insert_query

from models import users, players, requests
from common.exceptions import NotFound, BadRequest

from services import players_service
from services.users_service import get_user_by_id
from emails.send_emails import send_director_accept_email_async

def send_director_request(current_user: users.User):
    sql = """
        INSERT INTO director_requests(user_id, email, status)
        VALUES(?, ?, ?)
    """
    sql_params = (current_user.id, current_user.email, "pending")
    insert_query(sql, sql_params)


def get_director_requests():
    sql = "Select * FROM director_requests"
    sql_params = ()

    result = read_query(sql, sql_params)
    director_requests = [
        requests.DirectorRequest.from_query_result(
            id=row[0],
            user_id=row[1],
            email=row[2],
            status=row[3],
            created_at=row[4]
        ) 
        for row in result
    ]
    return director_requests


async def accept_director_request(request_id: int):
    director_request = get_director_request_by_id(request_id)
    if not director_request:
        raise NotFound("Director request not found")

    update_director_request_status(request_id, "accepted")
    update_user_to_player(director_request.user_id, "director")
    
    user_data = get_user_by_id(director_request.user_id)

    subject = "Director Acceptance Notification"
    email_to = user_data.email
    body = {
        "title": "Congratulations! You're now a Director.",
        "name": user_data.username,
        "ctaLink": f"http://localhost:3000/"
    }
    await send_director_accept_email_async(subject, email_to, body)


def reject_director_request(request_id: int):
    player_request = get_director_request_by_id(request_id)

    if not player_request:
        raise NotFound("Player request not found")

    update_director_request_status(request_id, "rejected")


def send_link_to_player_request(current_user: users.User, full_name: str):
    sql = """
        INSERT INTO link_player_requests(user_id, username, requested_full_name, status)
        VALUES(?, ?, ?, ?)
    """
    sql_params = (current_user.id, current_user.username, full_name, "pending")
    insert_query(sql, sql_params)


def get_link_requests():
    sql = "SELECT * FROM link_player_requests"
    sql_params = ()

    result = read_query(sql, sql_params)
    link_player_requests = [
        requests.LinkToPlayerRequest.from_query_result(
            id=row[0],
            user_id=row[1],
            username=row[2],
            requested_full_name=row[3],
            status=row[4],
            created_at=row[5]
        )
        for row in result
    ]

    return link_player_requests


def accept_link_player_request(request_id: int, current_user: users.User):
    link_player_request = get_link_player_request_by_id(request_id)
    if not link_player_request:
        raise NotFound("Link player request not found")

    if players_service.get_player_by_user_id(current_user.id):
        raise BadRequest("User is already linked to a player") 

    player = get_player_by_full_name(link_player_request.requested_full_name)
    if not player:
        raise NotFound(f"Player {link_player_request.requested_full_name} not found")

    update_link_player_request_status(request_id, "accepted")
    link_user_to_player(player, link_player_request.user_id)
    

def reject_link_player_request(request_id: int):
    link_player_request = get_link_player_request_by_id(request_id)
    if not link_player_request:
        raise NotFound("Link player request not found")

    update_link_player_request_status(request_id, "rejected")


def get_director_request_by_id(request_id: int):
    sql = """
        SELECT id, user_id, email, status, created_at
        FROM director_requests
        WHERE id = ?;
    """
    sql_params = (request_id,)
    result = read_query(sql, sql_params)
    if result:
        result = result[0]
        return requests.DirectorRequest.from_query_result(
            id=result[0],
            user_id=result[1],
            email=result[2],
            status=result[3],
            created_at=result[4]
        )
    
def get_link_player_request_by_id(request_id: int):
    sql = """
        SELECT id, user_id, username, requested_full_name, status, created_at
        FROM link_player_requests
        WHERE id = ?;
    """
    sql_params = (request_id,)
    result = read_query(sql, sql_params)
    if result:
        result = result[0]
        return requests.LinkToPlayerRequest.from_query_result(
            id=result[0],
            user_id=result[1],
            username=result[2],
            requested_full_name=result[3],
            status=result[4],
            created_at=result[5]
        )


def update_director_request_status(request_id, status):
    sql = """
        UPDATE director_requests
        SET status = ?
        WHERE id = ?;
    """
    sql_params = (status, request_id)
    insert_query(sql, sql_params)


def update_link_player_request_status(request_id, status):
    sql = """
        UPDATE link_player_requests
        SET status = ?
        WHERE id = ?
    """
    sql_params = (status, request_id)
    insert_query(sql, sql_params)


def update_user_to_player(user_id:int, role: str):
    sql = """
        UPDATE users
        SET role = ?
        WHERE id = ?;
    """
    sql_params = (role, user_id)
    insert_query(sql, sql_params)

def link_user_to_player(player: players.PlayerProfile, user_id: int):
    sql = """
        UPDATE players
        SET user_id = ?
        WHERE full_name = ?
    """
    sql_params = (user_id ,player.full_name)
    insert_query(sql, sql_params)

def get_player_by_full_name(full_name:str):
    sql = """
        SELECT id, full_name, country, sports_club, user_id
        FROM players
        WHERE full_name = ?
    """
    sql_params = (full_name,)
    result = read_query(sql, sql_params)
    if result:
        result = result[0]
        return players.PlayerProfile.from_query_result(
            id=result[0],
            full_name=result[1],
            country=result[2],
            sports_club=result[3],
            user_id=result[4]
        )