from models import tournaments

from database.database import insert_query, read_query
from models.users import User
from models.tournaments import Owner

def create(
    tournament_data: tournaments.TournamentCreate,
    current_user: User
):
    sql = """
        INSERT INTO tournaments (format, title, description, match_format, rounds, third_place, status, location, start_date, end_date, owner_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    sql_params = (
        tournament_data.format.value,
        tournament_data.title,
        tournament_data.description,
        tournament_data.match_format.value,
        tournament_data.rounds,
        tournament_data.third_place,
        tournament_data.status.value,
        tournament_data.location,
        tournament_data.start_date,
        tournament_data.end_date,
        current_user.id
    )


    created_tournament_id = insert_query(sql, sql_params)
    owner = get_owner_data_by_id(current_user.id)
    response_data = tournaments.Tournament(
        id=created_tournament_id,
        format=tournament_data.format, 
        title = tournament_data.title,
        description = tournament_data.description,
        match_format = tournament_data.match_format,
        rounds =  tournament_data.rounds,
        third_place = tournament_data.third_place,
        status = tournament_data.status,
        location = tournament_data.location,
        start_date = tournament_data.start_date,
        end_date = tournament_data.end_date,
        owner=owner
    )

    return response_data


def get_all():
    sql = """
            SELECT t.*, u.username, u.profile_img
            FROM tournaments t
            JOIN users u ON t.owner_id = u.id
            ORDER BY t.start_date;
        """
    sql_params = ()

    result = read_query(sql, sql_params)
    tournaments_data = []
    for row in result:
        owner = Owner(id=row[11], username=row[12], profile_img=row[13])
        tournament = tournaments.Tournament(
            id=row[0],
            format=row[1], 
            title = row[2],
            description= row[3],
            match_format = row[4],
            rounds =  row[5],
            third_place = row[6],
            status = row[7],
            location = row[8],
            start_date = str(row[9]),
            end_date = str(row[10]),
            owner = owner
        )
        tournaments_data.append(tournament)

    return tournaments_data

def get_one(tournament_id):
    sql = """
            SELECT t.*, u.username, u.profile_img
            FROM tournaments t
            JOIN users u ON t.owner_id = u.id
            WHERE t.id = ?
        """
    
    sql_params = (tournament_id,)

    result = read_query(sql, sql_params)

    if result:
        result = result[0]
        owner = Owner(id=result[11], username=result[12], profile_img=result[13])
        tournament = tournaments.Tournament(
            id=result[0],
            format=result[1], 
            title = result[2],
            description = result[3],
            match_format = result[4],
            rounds =  result[5],
            third_place = result[6],
            status = result[7],
            location = result[8],
            start_date = str(result[9]),
            end_date = str(result[10]),
            owner = owner
        )

        return tournament


def get_owner_data_by_id(owner_id):
    sql = """
            SELECT username, profile_img 
            FROM users WHERE id = ?;
        """
    sql_params = (owner_id,)

    result = read_query(sql, sql_params)
    if result: 
        user = Owner(
            id=owner_id,
            username=result[0][0],
            profile_img=result[0][1]
        )
        return user
        

def get_format(id: int):
    data = read_query('SELECT format FROM  tournaments WHERE id = ?', (id,))
    return data[0][0]
