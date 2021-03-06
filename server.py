from socketio import *
from gevent import pywsgi
from server_functions import *
import ast
import termcolor
server = Server(async_mode='gevent')


# ------------------------ Sign Up ------------------------

@server.on('add_user')
def add_user(sid, user_data):

    with open('database_file.txt', 'r') as f_read_database:
        database = f_read_database.read()
    database = ast.literal_eval(database)

    database.update(user_data)

    with open('database_file.txt', 'w') as f_write_database:  # update database file
        f_write_database.write(str(database))


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


# ------------------------ Login ------------------------

@server.on('ckeck_login_info')
def ckeck_login_info(sid, login_info):

    with open('database_file.txt') as f_read_database:
        database = f_read_database.read()
    database = ast.literal_eval(database)

    check_l = is_login_info_valid(login_info, database)

    if check_l:
        add_new_sid_to_username_record(sid, login_info)

    return check_l


# ------------------------ Leader Board ------------------------

@server.on('give_leader_board')
def give_leader_board(sid):

    with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
        leader_board = f_read_leaderboard.read()
    leader_board = ast.literal_eval(leader_board)

    sorted_leader_board = []
    wins_value_list = []
    for k in leader_board:  # Creating a list of all wins value
        wins_value_list.append(leader_board[k]['wins'])

    wins_value_list.sort(reverse=True)  # reverse it

    for i in wins_value_list:  # create a list of sorted record in leader board
        for k in leader_board:
            if leader_board[k]['wins'] == i:
                record = {k: leader_board[k]}
                sorted_leader_board.append(record)

    res = []
    [res.append(x) for x in sorted_leader_board if x not in res]
    server.emit('get_leader_board', res, room=sid)


# ------------------------ RTBF ------------------------

@server.on('get_rtbf_req')
def get_rtbf_req(sid, account_info):

    with open('database_file.txt') as f_read_database:
        database = f_read_database.read()
    database = ast.literal_eval(database)

    check_l = is_login_info_valid(account_info, database)
    if check_l:
        delete_user_data(sid, account_info)

        server.emit('get_rtbf_resp', True, room=sid)

    else:
        server.emit('get_rtbf_resp', False, room=sid)


# ------------------------ Game ------------------------
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

pieces_data = []


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
    Big_blue_hallowtop_square_ = termcolor.colored('???', 'blue')
    Big_yellow_hallowtop_square_ = termcolor.colored('???', 'yellow')
    Small_blue_hallowtop_square_ = termcolor.colored('???', 'blue')
    Small_yellow_hallowtop_square_ = termcolor.colored('???', 'yellow')
    Little_yellow_solid_square_ = termcolor.colored('???', 'yellow')
    Little_blue_solid_square_ = termcolor.colored('???', 'blue')
    Small_blue_little_circle_ = termcolor.colored('???', 'blue')
    Small_yellow_little_circle_ = termcolor.colored('???', 'yellow')
    Big_blue_hallowtop_circle_ = termcolor.colored('???', 'blue')
    Big_yellow_hallowtop_circle_ = termcolor.colored('???', 'yellow')
    Small_blue_hallowtop_circle_ = termcolor.colored('???', 'blue')
    Small_yellow_hallowtop_circle_ = termcolor.colored('???', 'yellow')
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
    dic.update({number: (shape, shapes[shape])})
    table = place_table(dic)

    server.emit('get_board', table)

    if not win_condition(dic):
        # ----------- START updating database for "tie" condition------
        if not movenumbers_can_choose:
            # ---------- start updating leaderboard for the first player ------------------------
            with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
                leader_board = f_read_leaderboard.read()
            leader_board = ast.literal_eval(leader_board)

            with open('sid_username_file.txt', 'r') as f_read_sid:
                sid_username_dic = f_read_sid.read()
            sid_username_dic = ast.literal_eval(sid_username_dic)

            leader_board.update({sid_username_dic[player_did_last_move[0]]: {'wins': leader_board[sid_username_dic[player_did_last_move[0]]]
                                                                             ['wins'], 'losses': leader_board[sid_username_dic[player_did_last_move[0]]]['losses'], 'tie': leader_board[sid_username_dic[player_did_last_move[0]]]['tie']+1}})
            # ------------- start updating leaderboard for the second player ------------------------
            for i in ready_players:
                if i != player_did_last_move[0]:
                    leader_board.update({sid_username_dic[i]: {'wins': leader_board[sid_username_dic[i]]
                                                               ['wins'], 'losses': leader_board[sid_username_dic[i]]['losses'], 'tie': leader_board[sid_username_dic[i]]['tie']+1}})
                    with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                        f_write_leaderboard.write(str(leader_board))
            server.emit('tie')
            delete_ready_players_to_free_server()

        # ---------- END updating leaderboard for the first player ------------------------

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
                # ------------- start updating leaderboard for loser ------------------------
                for i in ready_players:
                    if i != player_did_last_move[0]:
                        leader_board.update({sid_username_dic[i]: {'wins': leader_board[sid_username_dic[i]]
                                                                   ['wins'], 'losses': leader_board[sid_username_dic[i]]['losses']+1, 'tie': leader_board[sid_username_dic[i]]['tie']}})
                        with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                            f_write_leaderboard.write(str(leader_board))
                        server.emit(
                            'i_lost', 'OH! You lost the game...', room=i)
                        delete_ready_players_to_free_server()

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
                # ------------- start updating leaderboard for loser ------------------------
                for i in ready_players:
                    if i != player_did_last_move[0]:
                        leader_board.update({sid_username_dic[i]: {'wins': leader_board[sid_username_dic[i]]
                                                                   ['wins'], 'losses': leader_board[sid_username_dic[i]]['losses']+1, 'tie': leader_board[sid_username_dic[i]]['tie']}})
                        with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                            f_write_leaderboard.write(str(leader_board))
                        server.emit(
                            'i_lost', 'OH! You lost the game...', room=i)
                        delete_ready_players_to_free_server()

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
            # ------------- start updating leaderboard for loser ------------------------
            for i in ready_players:
                if i != player_did_last_move[0]:
                    leader_board.update({sid_username_dic[i]: {'wins': leader_board[sid_username_dic[i]]
                                                               ['wins'], 'losses': leader_board[sid_username_dic[i]]['losses']+1, 'tie': leader_board[sid_username_dic[i]]['tie']}})
                    with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                        f_write_leaderboard.write(str(leader_board))
                    server.emit(
                        'i_lost', 'OH! You lost the game...', room=i)
                    delete_ready_players_to_free_server()
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

            # ------------- start updating leaderboard for loser ------------------------
            for i in ready_players:
                if i != player_did_last_move[0]:
                    leader_board.update({sid_username_dic[i]: {'wins': leader_board[sid_username_dic[i]]
                                                               ['wins'], 'losses': leader_board[sid_username_dic[i]]['losses']+1, 'tie': leader_board[sid_username_dic[i]]['tie']}})
                    with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                        f_write_leaderboard.write(str(leader_board))
                    server.emit(
                        'i_lost', 'OH! You lost the game...', room=i)
                    delete_ready_players_to_free_server()
            return game

    return game
# ------------- checks that all items in foo have any common char ------------ #


def main_game():
    id_ = ready_players[0]

    request_choosen_piece(id_)


# ------------------------ After Game ----------------------------

def delete_ready_players_to_free_server():
    global ready_players
    global pieces
    global movenumbers_can_choose
    global count
    global can_start_game
    global piece_to_move
    global shape_to_move
    global player_did_last_move
    global dic

    can_start_game = False
    pieces = ['bbss', 'byss', 'sbss', 'syss', 'bbhs', 'byhs', 'sbhs',
              'syhs', 'bbsc', 'bysc', 'sbsc', 'sysc', 'bbhc', 'byhc', 'sbhc', 'syhc']
    count = 2
    piece_to_move = []
    shape_to_move = []
    movenumbers_can_choose = ['1', '2', '3', '4', '5', '6', '7',
                              '8', '9', '10', '11', '12', '13', '14', '15', '16']
    ready_players = []

    player_did_last_move = []
    dic = {}
    for i in range(1, 17):
        dic[i] = ('empty', '  ')


# -------------------------- Connect ----------------------------

@server.event  # ye baksh ke migim client mitone behet etelaat bede
def connect(sid, environ, auth):
    print(sid, "connected!")
    print(environ['REMOTE_PORT'])  # !1


# -------------------------- Disconnect ------------------------
@server.event
def disconnect(sid):
    flag8 = False
    if sid in ready_players:
        for player in ready_players:
            if player != sid and player != None:
                server.emit('i_won', 'The other player has left the game! You won!',
                            room=player)
                # ---------- start updating leaderboard for winner ------------------------
                with open('leaderboard_file.txt', 'r') as f_read_leaderboard:
                    leader_board = f_read_leaderboard.read()
                leader_board = ast.literal_eval(leader_board)

                with open('sid_username_file.txt', 'r') as f_read_sid:
                    sid_username_dic = f_read_sid.read()
                sid_username_dic = ast.literal_eval(sid_username_dic)

                leader_board.update({sid_username_dic[player]: {'wins': leader_board[sid_username_dic[player]]
                                                                                    ['wins']+1, 'losses': leader_board[sid_username_dic[player]]['losses'], 'tie': leader_board[sid_username_dic[player]]['tie']}})
                flag8 = True
        if flag8:
            # ------------- start updating leaderboard for loser ------------------------
            leader_board.update({sid_username_dic[sid]: {'wins': leader_board[sid_username_dic[sid]]
                                                         ['wins'], 'losses': leader_board[sid_username_dic[sid]]['losses']+1, 'tie': leader_board[sid_username_dic[sid]]['tie']}})
            with open('leaderboard_file.txt', 'w') as f_write_leaderboard:
                f_write_leaderboard.write(str(leader_board))

            delete_ready_players_to_free_server()

    print(sid, 'Disconnect ')


app = WSGIApp(server)

pywsgi.WSGIServer(("127.0.0.1", 5000), app).serve_forever()
