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
