from database.database import insert_query, read_query, update_query
from models.players import PlayerCreate, PlayerRequest, PlayerProfile, PlayerProfileImg
from models.enums import Request
from models.users import User
from common.exceptions import NotFound
from common.responses import RequestCreate
from common.utils import save_image

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


def accept_player_request(request_id: int):
    player_request = get_player_request_by_id(request_id)

    if not player_request:
        raise NotFound("Player request not found")

    update_player_request_status(request_id, Request.ACCEPTED.value)

    player_info = get_player_info_from_request(player_request)

    insert_player(player_request.requester_id, **player_info)


def reject_player_request(request_id: int):
    player_request = get_player_request_by_id(request_id)

    if not player_request:
        raise NotFound("Player request not found")

    update_player_request_status(request_id, Request.REJECTED.value)


def create_tournament_join_request_no_player(
        tournament_id: int,
        player_data: PlayerCreate,
        current_user: User
):
    sql = """
        INSERT INTO tournament_requests 
        (player_id, tournament_id, user_id, full_name, country, sports_club, status) 
        VALUES (NULL, ?, ?, ?, ?, ?, 'pending')
    """
    sql_params = (
        tournament_id,
        current_user.id,
        player_data.full_name,
        player_data.country,
        player_data.sports_club
    )

    insert_query(sql, sql_params)


def create_tournament_join_request_with_player(
        tournament_id: int,
        player_data: PlayerProfile,
):
    sql = """
        INSERT INTO tournament_requests 
        (player_id, tournament_id, user_id, full_name, country, sports_club, status) 
        VALUES (?, ?, NULL, ?, ?, ?, 'pending')
    """
    sql_params = (
        player_data.id,
        tournament_id,
        player_data.full_name,
        player_data.country,
        player_data.sports_club,
    )

    insert_query(sql, sql_params)


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


def insert_player(user_id: int, full_name: str, country: str, sports_club: str):
    sql = """
        INSERT INTO players (user_id, full_name, country, sports_club)
        VALUES (?, ?, ?, ?);
    """
    sql_params = (user_id, full_name, country, sports_club)
    return insert_query(sql, sql_params)


def get_player_by_user_id(user_id: int):
    sql = "SELECT id, full_name, country, sports_club FROM players WHERE user_id = ?;"
    sql_params = (user_id,)

    result = read_query(sql, sql_params)

    if result:
        id, full_name, country, sports_club = result[0]

        return PlayerProfile.from_query_result(
            id, full_name, country, sports_club
        )


def get_by_id(id: int):
    data = read_query('SELECT * FROM players WHERE id = ?', (id,))
    return next((PlayerProfileImg.from_query_result(*row) for row in data), None)


def update(
        target_player: PlayerProfileImg,
        full_name: str,
        country: str,
        sports_club: str,
        profile_img_path: str
):
    

    sql = """
        UPDATE players
        SET full_name = ?, country = ?, sports_club = ?, profile_img = ?
        WHERE id = ?
    """
    sql_params = (
        full_name,
        country,
        sports_club,
        profile_img_path,
        target_player.id
    )

    update_query(sql, sql_params)

    return get_by_id(target_player.id)




def count():
    data = read_query('SELECT COUNT(*) FROM players')
    return data[0][0]


def all(parameters: tuple):
    offset, limit = parameters

    data = read_query('''SELECT id, full_name, country, sports_club, profile_img
                                FROM players ORDER BY id LIMIT ? OFFSET ?''', (limit, offset))

    return (PlayerProfileImg.from_query_result(*row) for row in data)


def get_player_by_full_name(full_name: str):
    sql = """SELECT *
            FROM players 
            WHERE full_name = ?    
        """
    sql_params = (full_name,)

    result = read_query(sql, sql_params)
    if result:
        return PlayerProfileImg.from_query_result(*result[0])


def handle_profile_image(profile_image):
    if isinstance(profile_image, str):
        profile_image_path = profile_image
    else:
        profile_image_path = save_image(profile_image, "players_pics")

    return profile_image_path
