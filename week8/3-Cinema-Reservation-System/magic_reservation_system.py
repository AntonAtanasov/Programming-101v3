import readline
from tabulate import tabulate


class CinemaReservation:

    HALL_ROWS = 10
    HALL_COLS = 10
    HALL_SEATS = HALL_ROWS * HALL_COLS

    GET_MOVIES_BY_RATING = '''SELECT * FROM Movies
        ORDER BY rating DESC
    '''

    GET_PROJECTIONS = '''SELECT Projections.*,
        (SELECT name FROM Movies WHERE Movies.id = Projections.movie_id),
        ? - (SELECT COUNT(id) FROM Reservations WHERE Reservations.projection_id = Projections.id) AS free_seats FROM Projections
        WHERE movie_id LIKE ? AND projection_date LIKE ?
        ORDER BY projection_date ASC
    '''

    GET_TAKEN_SEATS_FOR_PROJ = '''SELECT row, col FROM Reservations WHERE projection_id = ?'''

    GET_IDS_FROM_PROJ = '''SELECT id FROM Projections where movie_id = ?'''

    GET_RESERV_INF = '''SELECT Projections.projection_date, Projections.projection_time,
        Projections.type, Movies.name FROM Projections
        JOIN Movies ON Projections.movie_id == Movies.id WHERE Projections.id = ?
    '''

    MAKE_RESERVE = '''INSERT INTO Reservations(username, projection_id, row, col) VALUES(?, ?, ?, ?)'''
    GET_RESERVE_BY_USER = '''SELECT * FROM Reservations WHERE username is ? AND projection_ID = ?'''
    DELETE_RESERVE = '''DELETE FROM Reservations WHERE username is ? AND projection_ID = ?'''

    @staticmethod
    def create_help():
        help = ["Here is the list of commands:",
                "",
                "show_movies                             : Prints all movies ORDERed BY rating",
                "show_projections <movie_id> [<date>]>   : Prints all projections of a given movie for the given date (date is optional).",
                "make_reservation                        : Starts the reservation proccess",
                "cancel_reservation <projection>         : Disintegrate given person's reservation",
                "exit                                    : Exits reservation system"]
        return "\n".join(help)

    @staticmethod
    def parse_command(command):
        return tuple(command.split(" "))

    @staticmethod
    def is_command(command_tuple, command_string):
        return command_tuple[0] == command_string

    @staticmethod
    def trigger_unknown_command():
        unknown_command = ["Error: Unknown command!",
                           "Why don't you type help,",
                           "to see a list of commands."]

        return "\n".join(unknown_command)

    @classmethod
    def show_movies(cls, connection):
        cursor = connection.cursor()
        cursor.execute(cls.GET_MOVIES_BY_RATING)
        movies_by_rating = cursor.fetchall()
        headers = ["id", "Movie Name", "Movie Rating"]
        table_cols = [0, 1, 2]
        return cls.make_tabulate_tabl(headers, table_cols, movies_by_rating)

    @classmethod
    def show_movie_projections(cls, connection, movie_id='%%', date='%%'):
        cursor = connection.cursor()

        cursor.execute(cls.GET_PROJECTIONS, (cls.HALL_SEATS, movie_id, date))
        projections_by_movie = cursor.fetchall()

        if not projections_by_movie:
            return False

        headers = ["id", "date", "time", "type", "movie_name", "free_seats"]
        table_cols = [0, 3, 4, 2, 5, 6]
        return cls.make_tabulate_tabl(headers, table_cols, projections_by_movie)

    @classmethod
    def show_hall_layout(cls, connection, projection_id):
        headers = ['R/C']
        headers += ['C-{}'.format(i+1) for i in range(cls.HALL_COLS)]
        table_cols = [i for i in range(cls.HALL_COLS + 1)]
        data = []

        taken_seats = cls.get_taken_seats_by_proj(connection, projection_id)

        for row in range(cls.HALL_ROWS):
            data.append(['R-{}'.format(row + 1)])
            for col in range(cls.HALL_COLS + 1):
                if (row+1, col+1) in taken_seats:
                    data[row].append('_X_')
                else:
                    data[row].append('FREE')
        return cls.make_tabulate_tabl(headers, table_cols, data)

    @classmethod
    def make_tabulate_tabl(cls, headers, table_cols, table_data):
        pptable = []
        for row in table_data:
            pptable.append([row[i] for i in table_cols])
        return tabulate(pptable, headers, tablefmt="fancy_grid")

    @classmethod
    def get_id_of_projections(cls, connection, movie_id):
        cursor = connection.cursor()
        cursor.execute(cls.GET_IDS_FROM_PROJ, (movie_id, ))
        return cursor.fetchall()

    @classmethod
    def get_taken_seats_by_proj(cls, connection, proj_id):
        cursor = connection.cursor()
        cursor.execute(cls.GET_TAKEN_SEATS_FOR_PROJ, (proj_id, ))
        return cursor.fetchall()

    @classmethod
    def get_reservation_info(cls, connection, usr_data):
        proj_id = usr_data['Step-4']
        seats = usr_data['Step-5']
        headers = ['Date', 'Time', 'Type', 'Movie', 'Seats']
        table_cols = [0, 1, 2, 3, 4]

        cursor = connection.cursor()
        cursor.execute(cls.GET_RESERV_INF, (proj_id, ))
        data = cursor.fetchall()
        data[0] += (seats, )
        return cls.make_tabulate_tabl(headers, table_cols, data)

    @classmethod
    def make_reservation(cls, connection, reservation_data):
        user = reservation_data['Step-1']
        projection = reservation_data['Step-4']
        seats = reservation_data['Step-5']

        cursor = connection.cursor()

        for seat in seats:
            row, col = seat
            cursor.execute(cls.MAKE_RESERVE, (user, projection, row, col))

        connection.commit()
        return ('Your Reservation Was Successful')

    @classmethod
    def cancel_reservation(cls, connection, projection, user):
        cursor = connection.cursor()
        cursor.execute(cls.GET_RESERVE_BY_USER, (user, projection))
        reservations = cursor.fetchall()

        if reservations:
            cursor.execute(cls.DELETE_RESERVE, (user, projection))
            connection.commit()
            return 'Your Reservation Was DELETED!'
        return 'No such reservation!'
