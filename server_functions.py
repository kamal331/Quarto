import ast


def is_uname_valid(user_name, database):
    if len(user_name) <= 3:
        return False

    for char in user_name:  # space and sumbols must not be in user_name.
        if char in ''' !@#$%^&*()-=+`~|}]{['"?/\.<:;,''':
            print('user name must not include any symbols (except "_")')
            return False

    if user_name in database:
        return False

    return True


def is_login_info_valid(login_info, database):
    login_check = False
    for k_login in login_info:
        for k_database in database:
            if k_login == k_database:
                if login_info[k_login]['password'] == database[k_database]['password']:
                    login_check = True

    return login_check


def add_new_sid_to_username_record(sid, login_info):
    with open('sid_username_file.txt', 'r') as f_read_sid:
        sid_username_dic = f_read_sid.read()
    sid_username_dic = ast.literal_eval(sid_username_dic)

    for u in login_info:
        new_record = {sid: u}  # {sid : user}

    sid_username_dic.update(new_record)

    with open('sid_username_file.txt', 'w') as f_write_sid:
        f_write_sid.write(str(sid_username_dic))


def delete_user_data(sid, account_info):
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
    # ------------------ Delete fro sid_usernam_dic -----------------

    with open('sid_username_file.txt', 'r') as f_read_sid:  # open dic
        sid_username_dic = f_read_sid.read()
    sid_username_dic = ast.literal_eval(sid_username_dic)

    for u in account_info:
        for k in sid_username_dic:
            if sid_username_dic[k] == u:
                del sid_username_dic[k]  # delete all sid record

    with open('sid_username_file.txt', 'w') as f_write_sid:  # re-write new dic
        f_write_sid.write(str(sid_username_dic))


# ------------------------ game ---------------------------
def place_table(dic):
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
