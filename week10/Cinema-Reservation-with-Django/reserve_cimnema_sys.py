from magic_reservation_system import CinemaReservation
from settings import DB_NAME
import sqlite3
import copy

reserve_msg = [("Step 1(user)>", str),
               ("Step 2(number of tickets)>", int),
               ("Step 3(choose a movie)>", int),
               ("Step 4(choose projection)>", int),
               ("Step 5(choose seats for ", tuple),
               ("Step 6(Confirm - type 'finalize')>", str)]


db_connection = sqlite3.connect(DB_NAME)


def main():

    while True:
        command = CinemaReservation.parse_command(input("Enter command>"))

        if CinemaReservation.is_command(command, "help"):
            print(CinemaReservation.create_help())

        elif CinemaReservation.is_command(command, "show_movies"):
            print (CinemaReservation.show_movies(db_connection))

        elif CinemaReservation.is_command(command, "show_projections"):
            if len(command) == 3:
                print(CinemaReservation.show_movie_projections(db_connection, command[1], command[2]))
            elif len(command) == 2:
                print(CinemaReservation.show_movie_projections(db_connection, command[1]))
            else:
                print(CinemaReservation.show_movie_projections(db_connection))

        elif CinemaReservation.is_command(command, "make_reservation"):
            print ('You are about to make reservation! Just folloow the steps. You can give_up @ any time :)')
            user_data = reservation_flow()
            if user_data:
                print(CinemaReservation.make_reservation(db_connection, user_data))

        elif CinemaReservation.is_command(command, "cancel_reservation"):
            if len(command) != 2:
                print('Projection ID not given')
                continue
            user = input("User?>")
            print (CinemaReservation.cancel_reservation(db_connection, command[1], user))

        elif CinemaReservation.is_command(command, "exit"):
            db_connection.close()
            break

        else:
            if command[0] is '':
                continue
            print(CinemaReservation.trigger_unknown_command())


def reservation_flow():
    recv_data = {}
    current_reservation = copy.deepcopy(reserve_msg)

    while current_reservation:

        current_step, data_type = current_reservation[0]
        current_reservation.pop(0)

        if current_step == reserve_msg[2][0]:
            cur_step_data = get_movie(current_step, data_type)

        elif current_step == reserve_msg[3][0]:
            cur_step_data = get_projection(current_step, data_type, recv_data['Step-3'], recv_data['Step-2'])

        elif current_step == reserve_msg[4][0]:
            cur_step_data = check_seats(recv_data['Step-2'], current_step, data_type, recv_data['Step-4'])

        elif current_step == reserve_msg[5][0]:
            cur_step_data = final_notice(current_step, data_type, recv_data)

        else:
            cur_step_data = take_user_data(current_step, data_type)

        if not cur_step_data:
            print ('Reservation process aborted!')
            return False

        step_key = len(reserve_msg) - len(current_reservation)
        recv_data['Step-{}'.format(step_key)] = cur_step_data

    return recv_data


def final_notice(step, data_type, usr_data):
    print('This is Sum-Up for your Reservation')
    print(CinemaReservation.get_reservation_info(db_connection, usr_data))
    is_fin_ok = take_user_data(step, data_type)
    if is_fin_ok in 'finalize':
        return is_fin_ok
    return False


def get_movie(step, data_type):
    print (CinemaReservation.show_movies(db_connection))
    movie_id = None
    while not CinemaReservation.show_movie_projections(db_connection, movie_id):
        movie_id = take_user_data(step, data_type)
        if not movie_id:
            return False
    return movie_id


def get_projection(step, data_type, movie_id, numb_tickets):
    print (CinemaReservation.show_movie_projections(db_connection, movie_id))
    l_id = []
    proj_ids = CinemaReservation.get_id_of_projections(db_connection, movie_id)
    for ids in proj_ids:
        l_id.append(ids[0])

    no_space = True
    proj_id = None
    while proj_id not in l_id or no_space:
        proj_id = take_user_data(step, data_type)
        taken_seats = CinemaReservation.get_taken_seats_by_proj(db_connection, proj_id)
        if numb_tickets > 100 - len(taken_seats):
            print ('There are not enough free seats for your reservation')
            continue
        no_space = False
        if not proj_id:
            return False
    return proj_id


def check_seats(numb_of_seats, step, d_type, proj_id):
    print (CinemaReservation.show_hall_layout(db_connection, proj_id))
    taken_seats = CinemaReservation.get_taken_seats_by_proj(db_connection, proj_id)

    seats = []
    for tick_num, seat in enumerate(range(numb_of_seats)):
        while True:
            try:
                data = input(step + 'Tiket-{}>'.format(tick_num + 1))
                if is_give_up(data):
                    return False
                seat_pos = d_type(int(x.strip()) for x in data.split(','))
                in_row = 0 < seat_pos[0] < 10
                in_col = 0 < seat_pos[1] < 10
                if seat_pos in taken_seats or not in_row or not in_col or seat_pos in seats:
                    print ('This seat is already taken Or Out of Range')
                    continue
                seats.append(seat_pos)
                break
            except Exception as e:
                print (e)
                continue

    return seats


def take_user_data(step, data_type):

    while True:
        try:
            data = input(step)
            if is_give_up(data):
                return False
            if not data:
                continue
            else:
                return data_type(data)
        except Exception as e:
            print(e)


def is_give_up(data):
    return data == 'give_up'

if __name__ == '__main__':
    main()
