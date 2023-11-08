from database.database import read_query, insert_query
from models.users import User, UserLoginResponse
from common.hashing import hash_password
from common.authorization import create_token


def register(user_data: User):
    username = user_data.username
    email = user_data.email
    password = hash_password(user_data.password)

    sql = "INSERT INTO users(username, email, password) values (?, ?, ?)"
    sql_params = (username, email, password)

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


def get_user_by_username(username):
    sql = "SELECT * FROM users WHERE username = ?"
    sql_params = (username,)

    result = read_query(sql, sql_params)
    if result:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "email": result[0][2],
            "player_id": result[0][4]
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
            "player_id": result[0][5]
        }
        return user


def get_user_by_id(user_id):
    sql = "SELECT * from users WHERE id = ?"
    sql_params = (user_id,)

    result = read_query(sql, sql_params)
    if result:
        user = {
            "id": result[0][0],
            "username": result[0][1],
            "email": result[0][2],
            "player_id": result[0][4],
        }
        return user


def passwords_match(pass1: str, pass2: str):
    return pass1 == pass2
