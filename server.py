from socketio import *
from gevent import pywsgi
from server_functions import *
import ast
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

    # chon room=sid nadare, be hame client ha ersal mikoneh? ya chon resp dare intor nist?
    return is_login_info_valid(login_info, database)

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
