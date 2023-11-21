from database.database import read_query
from models.users import User
from models.players import PlayerProfileImg
from models.tournaments import TournamentWithoutOwner

def get_users(username):
    if username:
        sql = "SELECT id, username, email, role, bio, profile_img, cover_img FROM users WHERE username LIKE ?"
        sql_params = ("%" + username + "%",)
    else:
        sql = "SELECT * FROM users"
        sql_params = ()

    result = read_query(sql, sql_params)

    user_data = []
    for row in result:
        user_data.append(User.from_query_result(*row))

    print(user_data)
    return user_data


def get_players(full_name):
    if full_name:
        sql = "SELECT * FROM players WHERE full_name LIKE ?"
        sql_params = ("%" + full_name + "%",)
    else:
        sql = "SELECT * FROM players"
        sql_params = ()

    result = read_query(sql, sql_params)

    players_data = []
    for row in result:
        players_data.append(PlayerProfileImg.from_query_result(*row))

    return players_data



def get_tournaments(title):
    if title:
        sql = "SELECT * FROM tournaments WHERE title LIKE ?"
        sql_params = ("%" + title + "%",)
    else:
        sql = "SELECT * FROM tournaments"
        sql_params = ()

    result = read_query(sql, sql_params)

    tournaments_data = []
    for row in result:
        tournaments_data.append(TournamentWithoutOwner.from_query_result(*row))

    return tournaments_data