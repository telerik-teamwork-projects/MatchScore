from database.database import read_query, insert_query, update_query

from models import users, players
from models.enums import Role
from models.requests import DirectorRequest
from common.hashing import hash_password
from common.authorization import create_token
from common.utils import save_image
from common.responses import RequestOK
from common.exceptions import NotFound

def register(user_data: users.User):
    username = user_data.username
    email = user_data.email
    password = hash_password(user_data.password)
    role = Role.USER

    sql = "INSERT INTO users(username, email, password, role) values (?, ?, ?, ?)"
    sql_params = (username, email, password, role.value)
    registered_user_id = insert_query(sql, sql_params)

    return get_user_by_id(registered_user_id)


def login(
        user: users.User
):
    token = create_token(user)

    return users.UserLoginResponse(
        token=token, user=user
    )


def update(
        target_user: users.User,
        username: str,
        email: str,
        bio: str,
        profile_image_path: str,
        cover_image_path: str,
):
    sql = """
        UPDATE users
        SET username = ?, email = ?, bio = ?, profile_img = ?, cover_img = ?
        WHERE id = ?
    """
    sql_params = (
        username,
        email,
        bio,
        profile_image_path,
        cover_image_path,
        target_user.id
    )

    update_query(sql, sql_params)

    return get_user_by_id(target_user.id)


def user_delete(
        target_user: users.User
):
    sql = "DELETE FROM users WHERE id = ?"
    sql_params = (target_user.id,)

    update_query(sql, sql_params)

    return RequestOK(f"Successfully deleted user: {target_user.username}")


def get_users(username):
    if username:
        sql = "SELECT * FROM users WHERE username LIKE ?"
        sql_params = ("%" + username + "%",)
    else:
        sql = "SELECT * FROM users"
        sql_params = ()

    result = read_query(sql, sql_params)

    user_data = []
    for row in result:
        user = users.User(
            id=row[0],
            username=row[1],
            email=row[2],
            role=row[4],
            bio=row[5],
            profile_img=row[6],
            cover_img=row[7],
        )
        user_data.append(user)
    return user_data


def get_director_requests():
    sql = "Select * FROM director_requests"
    sql_params = ()

    result = read_query(sql, sql_params)
    director_requests = [
        DirectorRequest(
            id=row[0],
            user_id=row[1],
            email=row[2],
            status=row[3],
            created_at=row[4]
        ) 
        for row in result
    ]
    return director_requests


def accept_director_request(request_id: int):
    director_request = get_director_request_by_id(request_id)
    if not director_request:
        raise NotFound("Director request not found")

    update_director_request_status(request_id, "accepted")
    update_user_to_player(director_request.user_id, "director")
    

def reject_director_request(request_id: int):
    player_request = get_director_request_by_id(request_id)

    if not player_request:
        raise NotFound("Player request not found")

    update_director_request_status(request_id, "rejected")


def get_user_by_username(username):
    sql = "SELECT * FROM users WHERE username = ?"
    sql_params = (username,)

    result = read_query(sql, sql_params)
    if result:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "email": result[0][2],
            "role": result[0][4],
            "bio": result[0][5],
            "profile_img": result[0][6],
            "cover_img": result[0][7],
        }
        return user


def get_user_by_email(email):
    sql = "SELECT * FROM users WHERE email = ?"
    sql_params = (email,)

    result = read_query(sql, sql_params)

    if result:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "email": result[0][2],
            "password": result[0][3],
            "role": result[0][4],
            "bio": result[0][5],
            "profile_img": result[0][6],
            "cover_img": result[0][7],
        }
        return user


def get_user_by_id(user_id):
    sql = "SELECT * from users WHERE id = ?"
    sql_params = (user_id,)

    result = read_query(sql, sql_params)
    if result:
        user = users.User.from_query_result(
            id=result[0][0],
            username=result[0][1],
            email=result[0][2],
            role=result[0][4],
            bio=result[0][5],
            profile_img=result[0][6],
            cover_img=result[0][7],
        )
        return user


def passwords_match(pass1: str, pass2: str):
    return pass1 == pass2


def handle_profile_image(profile_image):
    if isinstance(profile_image, str):
        profile_image_path = profile_image
    else:
        profile_image_path = save_image(profile_image, "profile_pics")

    return profile_image_path


def handle_cover_image(cover_image):
    if isinstance(cover_image, str):
        cover_image_path = cover_image
    else:
        cover_image_path = save_image(cover_image, "cover_pics")

    return cover_image_path


def get_director_request_by_id(request_id: int):
    sql = """
        SELECT id, user_id, email, status, created_at
        FROM director_requests
        WHERE id = ?;
    """
    sql_params = (request_id,)
    result = read_query(sql, sql_params)
    result = result[0]
    if result:
        return DirectorRequest(
            id=result[0],
            user_id=result[1],
            email=result[2],
            status=result[3],
            created_at=result[4]
        )
    

def update_director_request_status(request_id, status):
    sql = """
        UPDATE director_requests
        SET status = ?
        WHERE id = ?;
    """
    sql_params = (status, request_id)
    insert_query(sql, sql_params)


def update_user_to_player(user_id:int, status: str):
    sql = """
        UPDATE users
        SET role = ?
        WHERE id = ?;
    """
    sql_params = (status, user_id)
    insert_query(sql, sql_params)