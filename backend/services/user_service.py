from database.database import read_query, insert_query
from models.users import User, UserLoginResponse
from common.hashing import hash_password
from common.authorization import create_token
from models.enums import Role

def register(user_data: User):
    username = user_data.username
    email = user_data.email
    password = hash_password(user_data.password)
    role = Role.USER


    sql = "INSERT INTO users(username, email, password, role) values (?, ?, ?, ?)"
    sql_params = (username, email, password, role.value)
    registered_user_id = insert_query(sql, sql_params)
    
    user = get_user_by_id(registered_user_id)
    print(user)
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
            id = row[0],
            username =  row[1],
            email = row[2],
            role = row[4],
            player_id= row[5]
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
            "player_id": result[0][5]
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
        user = User (
            id = result[0][0],
            username = result[0][1],
            email = result[0][2],
            role =  result[0][4],
            player_id = result[0][5]
        )
        return user
    
def passwords_match(pass1: str, pass2:str):
    return pass1 == pass2