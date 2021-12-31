from socketio import *
from gevent import pywsgi

server = Server(async_mode='gevent')
# name_list = []  # (name, age)
# games = []  # [(name1, age1), (name2, age2)]
# users_data = {}

database = {'james_123': 1}


@server.on('add_user')
def add_user(sid, user_data):
    # while it wasn't exis: ask the user enter another user name
    # albate in bayad toye client darkhast ersal she hengam neveshtan user_name
    database.update(user_data)
    print(database)


@server.on('user_name_validity')
def user_name_validity(sid, user_name):  # for sign-up.
    if len(user_name) <= 3:
        return False

    for char in user_name:  # space and sumbols must not be in user_name.
        if char in ''' !@#$%^&*()-=+`~|}]{['"?/\.<:;,''':
            print('user name must not include any symbols (except "_")')
            return False

    if user_name in database:
        return False

    return user_name


@server.on('ckeck_login_info')
def ckeck_login_info(sid, login_info):
    # if login_info
    pass  # !!!!!!!!!!!!!!!!!


"""def _is_user_name_exist(user_name):
    for item in name_list:
        if name_list[0] == user_name:
            return True
    return False


def _get_age(user_name):
    for item in name_list:
        if name_list[0] == user_name:
            return name_list[1]"""


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
