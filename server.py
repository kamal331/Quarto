from asyncio import sleep
from asyncore import read
from dataclasses import dataclass
from http import client
from socketio import *
from gevent import pywsgi
from server_functions import *
import ast
import termcolor
server = Server(async_mode='gevent')
# name_list = []  # (name, age)
# games = []  # [(name1, age1), (name2, age2)]
# users_data = {}

""" Must me added
    Licence info
"""


@server.on('add_user')
def add_user(sid, user_data):

    with open('database_file.txt', 'r') as f_read_database:
        database = f_read_database.read()
    database = ast.literal_eval(database)

    # while it wasn't exis: ask the user enter another user name
    # albate in bayad toye client darkhast ersal she hengam neveshtan user_name
    database.update(user_data)

    with open('database_file.txt', 'w') as f_write_database:  # update database file
        f_write_database.write(str(database))

    print(database)  # delete after end **********


@server.on('user_name_validity')
def user_name_validity(sid, user_name):  # for sign-up.

    with open('database_file.txt', 'r') as f_read_database:
        database = f_read_database.read()
    database = ast.literal_eval(database)

    answer = is_uname_valid(user_name, database)
    server.emit('is_user_name_valid_resp', answer, room=sid)


@server.on('add_user_to_leader_board')
def add_user_to_leader_board(sid, leader_board_info):

    with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
        leader_board = f_read_leaderboard.read()
    leader_board = ast.literal_eval(leader_board)

    leader_board.update(leader_board_info)

    with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
        f_write_leaderboard.write(str(leader_board))

    print(leader_board)


@server.on('ckeck_login_info')
def ckeck_login_info(sid, login_info):

    with open('database_file.txt') as f_read_database:
        database = f_read_database.read()
    database = ast.literal_eval(database)

    check_l = is_login_info_valid(login_info, database)
    if check_l:

        with open('sid_username_file.txt', 'r') as f_read_sid:
            sid_username_dic = f_read_sid.read()
        sid_username_dic = ast.literal_eval(sid_username_dic)

        for u in login_info:
            new_record = {sid: u}  # {sid : user}

        sid_username_dic.update(new_record)

        with open('sid_username_file.txt', 'w') as f_write_sid:
            f_write_sid.write(str(sid_username_dic))

    # chon room=sid nadare, be hame client ha ersal mikoneh? ya chon resp dare intor nist?
    return check_l

    """ login_check = False
    for k_login in login_info:
        for k_database in database:
            if k_login == k_database:
                if login_info[k_login]['password'] == database[k_database]['password']:
                    login_check = True
    return login_check """


@server.on('give_leader_board')
def give_leader_board(sid):

    with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
        leader_board = f_read_leaderboard.read()
    leader_board = ast.literal_eval(leader_board)

    server.emit('get_leader_board', leader_board, room=sid)
# @server.on('send_pass_hash')
# def send_pass_hash(sid, user_name):  # room=player[0]
#    server.emit('get_pass_hash_resp', database[user_name]['password'])


@server.on('get_rtbf_req')
def get_rtbf_req(sid, account_info):

    with open('database_file.txt') as f_read_database:
        database = f_read_database.read()
    database = ast.literal_eval(database)

    check_l = is_login_info_valid(account_info, database)
    if check_l:
        # -------------------------delete from database-------------------------
        with open('database_file.txt', 'r') as f_read_database:
            database = f_read_database.read()
        database = ast.literal_eval(database)

        # while it wasn't exis: ask the user enter another user name
        # albate in bayad toye client darkhast ersal she hengam neveshtan user_name
        for u in account_info:
            del database[u]

        with open('database_file.txt', 'w') as f_write_database:  # update database file
            f_write_database.write(str(database))
        # -------------------------delete from leaderboard-----------------------
        with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
            leader_board = f_read_leaderboard.read()
        leader_board = ast.literal_eval(leader_board)

        for u in account_info:
            del leader_board[u]

        with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
            f_write_leaderboard.write(str(leader_board))
# --------------------------end deleting-----------------------------------
        server.emit('get_rtbf_resp', True, room=sid)

    else:
        server.emit('get_rtbf_resp', False, room=sid)


# ------------------------------------------------
ready_players = []
can_start_game = False


@server.on('give_ready_players')
def give_ready_players(sid, ready):

    if len(ready_players) >= 2:
        server.emit('can_i_join', False)
    else:
        ready_players.append(sid)
        if len(ready_players) == 2:
            main_game()


pieces = ['bbss', 'byss', 'sbss', 'syss', 'bbhs', 'byhs', 'sbhs',
          'syhs', 'bbsc', 'bysc', 'sbsc', 'sysc', 'bbhc', 'byhc', 'sbhc', 'syhc']
count = 2
piece_to_move = []
shape_to_move = []
movenumbers_can_choose = ['1', '2', '3', '4', '5', '6', '7',
                          '8', '9', '10', '11', '12', '13', '14', '15', '16']


def request_choosen_piece(id_):

    server.emit('choose_piece', pieces, room=id_)


@server.on('get_choosen_piece')
def get_choosen_piece(sid, choosed_piece):
    for i in ready_players:
        if i != sid:
            pieces.remove(choosed_piece)
            shape_to_move.append(choosed_piece)
            request_choosen_move(i, choosed_piece)


def request_choosen_move(sid, choosed_piece):
    give_choose_move_data = []
    give_choose_move_data.append(choosed_piece)
    give_choose_move_data.append(movenumbers_can_choose)
    server.emit('choose_move', give_choose_move_data, room=sid)


player_did_last_move = []
dic = {}
for i in range(1, 17):
    dic[i] = ('empty', '  ')


@server.on('get_choosen_move')
def get_choosen_move(sid, move):
    global count
    global movenumbers_can_choose
    global player_did_last_move
    global piece_to_move
    global shape_to_move
    Big_blue_hallowtop_square_ = termcolor.colored('□', 'blue')
    Big_yellow_hallowtop_square_ = termcolor.colored('□', 'yellow')
    Small_blue_hallowtop_square_ = termcolor.colored('⋄', 'blue')
    Small_yellow_hallowtop_square_ = termcolor.colored('⋄', 'yellow')
    Little_yellow_solid_square_ = termcolor.colored('▪', 'yellow')
    Little_blue_solid_square_ = termcolor.colored('▪', 'blue')
    Small_blue_little_circle_ = termcolor.colored('•', 'blue')
    Small_yellow_little_circle_ = termcolor.colored('•', 'yellow')
    Big_blue_hallowtop_circle_ = termcolor.colored('⦿', 'blue')
    Big_yellow_hallowtop_circle_ = termcolor.colored('⦿', 'yellow')
    Small_blue_hallowtop_circle_ = termcolor.colored('⚬', 'blue')
    Small_yellow_hallowtop_circle_ = termcolor.colored('⚬', 'yellow')
    Left_parantesis_ = termcolor.colored('(', 'cyan', attrs=['bold'])
    Right_parantesis_ = termcolor.colored(')', 'cyan', attrs=['bold'])
    shapes = {
        'bbss': '\U0001F7E6',
        'byss': '\U0001F7E8',
        'sbss': f'{Little_blue_solid_square_} ',
        'syss': f'{Little_yellow_solid_square_} ',
        'bbhs': f'{Big_blue_hallowtop_square_} ',
        'byhs': f'{Big_yellow_hallowtop_square_} ',
        'sbhs': f'{Small_blue_hallowtop_square_} ',
        'syhs': f'{Small_yellow_hallowtop_square_} ',
        'bbsc': '\U0001F535',
        'bysc': '\U0001F7E1',
        'sbsc': f'{Small_blue_little_circle_} ',
        'sysc': f'{Small_yellow_little_circle_} ',
        'bbhc': f'{Big_blue_hallowtop_circle_} ',
        'byhc': f'{Big_yellow_hallowtop_circle_} ',
        'sbhc': f'{Small_blue_hallowtop_circle_} ',
        'syhc': f'{Small_yellow_hallowtop_circle_} '
    }
    player_did_last_move = [sid]
    piece_to_move.append(move)
    number = move
    shape = shape_to_move[0]
    movenumbers_can_choose.remove(str(number))
    # while(number < 17):
    dic.update({number: (shape, shapes[shape])})
    table = palce_table(dic)

    # if count % 2 == 0:  # to seperate player1 and 2
    server.emit('get_board', table)

    # else:
    #    server.emit('get_board', table, room=ready_players[0])

    if not win_condition(dic):
        if not movenumbers_can_choose:
            server.emit('tie')
        piece_to_move = []
        shape_to_move = []

        player_did_last_move = []

        if count % 2 == 0:
            request_choosen_piece(ready_players[1])
        else:
            request_choosen_piece(ready_players[0])

        #number = piece_to_move[0]
        #shape = shape_to_move[0]

        count += 1


# ==========================================================


def palce_table(dic):
    board = ''
    second_time = False
    for i in range(1, 17, 4):
        if not second_time:
            board += f'''______ _____ _____ _____
|     |     |     |     |
| {dic[i][1]}  | {dic[i+1][1]}  | {dic[i+2][1]}  | {dic[i+3][1]}  |
|_____|_____|_____|_____|'''

        else:
            board += f'''
|     |     |     |     |
| {dic[i][1]}  | {dic[i+1][1]}  | {dic[i+2][1]}  | {dic[i+3][1]}  |
|_____|_____|_____|_____|'''

        second_time = True
    return board


def win_condition(dic):  # gives all Columns and Rows and Diameters to check table
    game = False                # if game = True Game is Won
# ----------------------------- gives all columns ---------------------------- #
    for i in range(1, 5):
        column = []
        flag1 = True
        for j in range(i, 17, 4):
            column.append(j)
            if dic[j][1] == "  ":  # if any item in column is empty no need to check
                flag1 = False
                break
        if flag1:
            game = check_table(column, game, dic)
            if game:
                server.emit('i_won', 'Nice! You won!',
                            room=player_did_last_move[0])
                # ---------- start updating leaderboard for winner ------------------------
                with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
                    leader_board = f_read_leaderboard.read()
                leader_board = ast.literal_eval(leader_board)

                with open('sid_username_file.txt', 'r') as f_read_sid:
                    sid_username_dic = f_read_sid.read()
                sid_username_dic = ast.literal_eval(sid_username_dic)

                leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                                 ['wins']+1, 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses'], 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']}})
                with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                    f_write_leaderboard.write(str(leader_board))
                # ------------- start updating leaderboard for loser ------------------------
                for i in ready_players:
                    if i != player_did_last_move[0]:
                        leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                                         ['wins'], 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses']+1, 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']}})
                        server.emit(
                            'i_lost', 'OH! You lost the game...', room=i)

                return game
# ------------------------------ gives all Rows ------------------------------ #
    for i in range(1, 17, 4):
        row = []
        flag1 = True
        for j in range(i, i+4):
            row.append(j)
            if dic[j][1] == "  ":  # if any item in Row is empty no need to check
                flag1 = False
                break
        if flag1:
            game = check_table(row, game, dic)

            if game:
                server.emit('i_won', 'Nice! You won!',
                            room=player_did_last_move[0])
                # ---------- start updating leaderboard for winner ------------------------
                with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
                    leader_board = f_read_leaderboard.read()
                leader_board = ast.literal_eval(leader_board)

                with open('sid_username_file.txt', 'r') as f_read_sid:
                    sid_username_dic = f_read_sid.read()
                sid_username_dic = ast.literal_eval(sid_username_dic)

                leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                                 ['wins']+1, 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses'], 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']}})
                with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                    f_write_leaderboard.write(str(leader_board))
                # ------------- start updating leaderboard for loser ------------------------
                for i in ready_players:
                    if i != player_did_last_move[0]:
                        leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                                         ['wins'], 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses']+1, 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']}})
                        server.emit(
                            'i_lost', 'OH! You lost the game...', room=i)
                return game
# ---------------------------- gives two Diameters --------------------------- #
    d1 = [1, 6, 11, 16]
    flag1 = True  # if any item in Diameter is empty no need to check
    for i in d1:
        if dic[i][1] == "  ":
            flag1 = False

    if flag1:
        game = check_table(d1, game, dic)
        if game:
            server.emit('i_won', 'Nice! You won!',
                        room=player_did_last_move[0])
            # ---------- start updating leaderboard for winner ------------------------
            with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
                leader_board = f_read_leaderboard.read()
            leader_board = ast.literal_eval(leader_board)

            with open('sid_username_file.txt', 'r') as f_read_sid:
                sid_username_dic = f_read_sid.read()
            sid_username_dic = ast.literal_eval(sid_username_dic)

            leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                             ['wins']+1, 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses'], 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']}})
            with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                f_write_leaderboard.write(str(leader_board))
            # ------------- start updating leaderboard for loser ------------------------
            for i in ready_players:
                if i != player_did_last_move[0]:
                    leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                                     ['wins'], 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses']+1, 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']}})
                    server.emit(
                        'i_lost', 'OH! You lost the game...', room=i)
            return game

    d2 = [4, 7, 10, 13]
    flag1 = True
    for i in d2:
        if dic[i][1] == "  ":
            flag1 = False

    if flag1:
        game = check_table(d2, game, dic)
        if game:
            server.emit('i_won', 'Nice! You won!',
                        room=player_did_last_move[0])
            # ---------- start updating leaderboard for winner ------------------------
            with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
                leader_board = f_read_leaderboard.read()
            leader_board = ast.literal_eval(leader_board)

            with open('sid_username_file.txt', 'r') as f_read_sid:
                sid_username_dic = f_read_sid.read()
            sid_username_dic = ast.literal_eval(sid_username_dic)

            leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                             ['wins']+1, 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses'], 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']}})
            with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                f_write_leaderboard.write(str(leader_board))
            # ------------- start updating leaderboard for loser ------------------------
            for i in ready_players:
                if i != player_did_last_move[0]:
                    leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                                     ['wins'], 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses']+1, 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']}})
                    server.emit(
                        'i_lost', 'OH! You lost the game...', room=i)
            return game

    return game
# ------------- checks that all items in foo have any common char ------------ #


def check_table(foo, game, dic):
    common = []
    for i in range(0, 4):
        if dic[foo[1]][0][i] == dic[foo[0]][0][i]:
            common.append(dic[foo[1]][0][i])
        else:
            common.append(0)

    for i in range(2, 4):
        for j in range(4):
            if common[j] == 0:
                continue
            else:
                if dic[foo[i]][0][j] == common[j]:
                    continue
                else:
                    common[j] = 0

    for i in common:
        if i != 0:
            game = True
            return game
    return game


def main_game():
    # global piece_to_move
    # global shape_to_move
    id_ = ready_players[0]

    request_choosen_piece(id_)


"""     Big_blue_hallowtop_square_ = termcolor.colored('□', 'blue')
    Big_yellow_hallowtop_square_ = termcolor.colored('□', 'yellow')
    Small_blue_hallowtop_square_ = termcolor.colored('⋄', 'blue')
    Small_yellow_hallowtop_square_ = termcolor.colored('⋄', 'yellow')
    Little_yellow_solid_square_ = termcolor.colored('▪', 'yellow')
    Little_blue_solid_square_ = termcolor.colored('▪', 'blue')
    Small_blue_little_circle_ = termcolor.colored('•', 'blue')
    Small_yellow_little_circle_ = termcolor.colored('•', 'yellow')
    Big_blue_hallowtop_circle_ = termcolor.colored('⦿', 'blue')
    Big_yellow_hallowtop_circle_ = termcolor.colored('⦿', 'yellow')
    Small_blue_hallowtop_circle_ = termcolor.colored('⚬', 'blue')
    Small_yellow_hallowtop_circle_ = termcolor.colored('⚬', 'yellow')
    Left_parantesis_ = termcolor.colored('(', 'cyan', attrs=['bold'])
    Right_parantesis_ = termcolor.colored(')', 'cyan', attrs=['bold'])
    shapes = {
        'bbss': '\U0001F7E6',
        'byss': '\U0001F7E8',
        'sbss': f'{Little_blue_solid_square_} ',
        'syss': f'{Little_yellow_solid_square_} ',
        'bbhs': f'{Big_blue_hallowtop_square_} ',
        'byhs': f'{Big_yellow_hallowtop_square_} ',
        'sbhs': f'{Small_blue_hallowtop_square_} ',
        'syhs': f'{Small_yellow_hallowtop_square_} ',
        'bbsc': '\U0001F535',
        'bysc': '\U0001F7E1',
        'sbsc': f'{Small_blue_little_circle_} ',
        'sysc': f'{Small_yellow_little_circle_} ',
        'bbhc': f'{Big_blue_hallowtop_circle_} ',
        'byhc': f'{Big_yellow_hallowtop_circle_}',
        'sbhc': f'{Small_blue_hallowtop_circle_} ',
        'syhc': f'{Small_yellow_hallowtop_circle_}'
    } """

# while not piece_to_move:  # avoid race conditon when it is empty
#    pass

"""number = piece_to_move[0]
    shape = shape_to_move[0]
    count = 2
    while(number < 17):
        dict.update({number: (shape, shapes[shape])})
        board = palce_table(dict)
        if count % 2 == 0:  # to seperate player1 and 2
            server.emit('get_board', board, room=ready_players[1])

        else:
            server.emit('get_board', board, room=ready_players[0])

        if win_condition(dict):
            break

        piece_to_move = []
        shape_to_move = []

        if count % 2 == 0:
            request_choosen_piece(ready_players[1])
        else:
            request_choosen_piece(ready_players[0])

        number = piece_to_move[0]
        shape = shape_to_move[0]

        count += 1
"""

# -----------------------------------------------------


@server.event  # ye baksh ke migim client mitone behet etelaat bede
def connect(sid, environ, auth):
    print(sid, "connected!")
    print(environ['REMOTE_PORT'])  # !1


"""@server.on('welcome')  # client sends data
def welcome(sid, data):
    user_name = data['user_name']
    age = data['age']
    print(user_name, age)
    name_list.append((user_name, age))
    if not _is_user_name_exist(user_name):
        name_list.append((user_name, age))
        return 'added successfully'
    else:
        return 'this user name exist, choose another one'
    # print(f'{sid}', 'said', data)


@server.on('get_status')
def get_status(sid, data):
    num_players = len(name_list)
    return num_players


@server.on('start_game')
def start_game(sid, data):  # {'user1':..., 'user2'...}
    user1 = data['user1']  # check kon user1 vojod dashter bashe
    user2 = data['user2']
    age1, age2 = _get_age(user1), _get_age(user2)
    games.append([(user1, age1), (user2, age2)])
    return f'game started between {user1} & {user2}'


@server.on('get_rival_age')
def get_rival_age(sid, user):
    for game in games:
        user1 = game[0]
        user2 = game[1]

        if user1[0] == user:
            return user2[1]
        elif user2[0] == user:
            return user1[1]
    return 'game not found'
"""

app = WSGIApp(server)

pywsgi.WSGIServer(("127.0.0.1", 5000), app).serve_forever()
