from database.database import read_query, insert_query, update_query

from models.users import User, UserLoginResponse
from models.enums import Role

from common.hashing import hash_password
from common.authorization import create_token
from common.utils import save_image
from common.responses import RequestOK


def register(user_data: User):
    username = user_data.username
    email = user_data.email
    password = hash_password(user_data.password)
    role = Role.USER

    sql = "INSERT INTO users(username, email, password, role) values (?, ?, ?, ?)"
    sql_params = (username, email, password, role.value)
    registered_user_id = insert_query(sql, sql_params)

    user = get_user_by_id(registered_user_id)

    response_data = User(
        **user
    )

    return response_data


def login(
        user: User
):
    token = create_token(user)

    return UserLoginResponse(
        token=token, user=user
    )


def update(
        target_user: User,
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
        target_user: User
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
        user = User(
            id=row[0],
            username=row[1],
            email=row[2],
            role=row[4],
            bio=row[5],
            profile_img=row[6],
            cover_img=row[7],
            player_id=row[8],
        )
        user_data.append(user)
    return user_data


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
            "player_id": result[0][8]
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
            "player_id": result[0][8]
        }
        return user


def get_user_by_id(user_id):
    sql = "SELECT * from users WHERE id = ?"
    sql_params = (user_id,)

    result = read_query(sql, sql_params)
    if result:
        user = User(
            id=result[0][0],
            username=result[0][1],
            email=result[0][2],
            role=result[0][4],
            bio=result[0][5],
            profile_img=result[0][6],
            cover_img=result[0][7],
            player_id=result[0][8],
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
