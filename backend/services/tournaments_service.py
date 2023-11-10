from models import tournaments

from database.database import insert_query, read_query

def create(
    tournament_data: tournaments.TournamentCreate, 
):
    sql = """
        INSERT INTO tournaments (format, title, match_format, rounds, third_place, status, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    sql_params = (
        tournament_data.format.value,
        tournament_data.title,
        tournament_data.match_format.value,
        tournament_data.rounds,
        tournament_data.third_place,
        tournament_data.status.value,
        tournament_data.start_date,
        tournament_data.end_date,
    )


    created_tournament_id = insert_query(sql, sql_params)
    response_data = tournaments.Tournament(
        id=created_tournament_id,
        format=tournament_data.format, 
        title = tournament_data.title,
        match_format = tournament_data.match_format,
        rounds =  tournament_data.rounds,
        third_place = tournament_data.third_place,
        status = tournament_data.status,
        start_date = tournament_data.start_date,
        end_date = tournament_data.end_date
    )

    return response_data


def get_all():
    sql = "SELECT * from tournaments"
    sql_params = ()

    result = read_query(sql, sql_params)

    tournaments_data = []
    for row in result:
        tournament = tournaments.Tournament(
            id=row[0],
            format=row[1], 
            title = row[2],
            match_format = row[3],
            rounds =  row[4],
            third_place = row[5],
            status = row[6],
            start_date = str(row[7]),
            end_date = str(row[8])
        )
        tournaments_data.append(tournament)

    return tournaments_data