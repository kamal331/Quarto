from client_functions import *
import termcolor
from socketio import *
from getpass import getpass
import os


client = Client()


@client.event
def connect():
    termcolor.cprint('connected', 'magenta', attrs=['bold'])


@client.event
def connect_error(data):
    termcolor.cprint('Connection failed', 'magenta', attrs=['bold'])


@client.event()
def disconnect():
    termcolor.cprint('Disconnected', 'magenta', attrs=['bold'])


def start_game_resp(response):
    print(response)


def confirm_pass(password, confirm_password):
    return password == confirm_password


check_user_name = False
is_check_user_name_done = False


def sign_up():
    global check_user_name
    global is_check_user_name_done
    sign_up_message()
    # user_name = input('User Name: ')
    while not check_user_name:
        is_check_user_name_done = False
        user_name = input(termcolor.colored(
            'User name: ', 'cyan', attrs=['bold']))
        s = is_user_name_valid(user_name)
        while not is_check_user_name_done:  # avoid race condition
            pass

    password = getpass(termcolor.colored(
        'Password: ', 'cyan', attrs=['bold']))  # getting hiden pass for security
    while not is_pass_Strong(password):
        termcolor.cprint('your password is not strong enough',
                         'yellow', attrs=['bold'])
        password = getpass(termcolor.colored(
            'enter your password again: ', 'cyan', attrs=['bold']))

    termcolor.cprint(
        'Nice! Confirm your password (enter it again): ', 'yellow', attrs=['bold'])
    confirm_password = getpass(termcolor.colored(
        'enter your password again: ', 'cyan', attrs=['bold']))

    while not confirm_pass(password, confirm_password):
        print('Sorry \U0001F613. second password you entered, doesn\'t match with first password')
        confirm_password = getpass(termcolor.colored(
            'enter your password again: ', 'cyan', attrs=['bold']))

    NOT_ = termcolor.colored('NOT', 'yellow', attrs=['bold'])
    E_mail_ = termcolor.colored('E-mail', 'cyan', attrs=['bold'])
    email = input(
        f'''{E_mail_}: (optional. You are {NOT_} forced to enter your e-mail address.
        It is your privacy. Respect your privacy. Don't give your personal info
        to anyone.(includes us \U0001F9F1))
        if you Don,t want, just enter "0": ''')
    while not email_validity(email):
        termcolor.cprint(
            'your e-mail is not valid. eneter another one.', 'yellow', attrs=['bold'])
        email = input(termcolor.colored('E-mail: ', 'cyan', attrs=['bold']))

    confirm = input(termcolor.colored(
        'Do you want to sign-up? write "yes". If you don\'t, write any other thing to back to the menu: ', 'cyan', attrs=['bold'])).lower()
    if confirm == 'yes':
        wins = 0
        losses = 0
        tie_ = 0
        leader_board_info = {}
        leader_board_info[user_name] = {
            'wins': wins,
            'losses': losses,
            'tie': tie_
        }
        client.emit('add_user_to_leader_board', leader_board_info)
        # we don't pass hashed password to server!
        password = pbkdf2_hash(password)
        user_data = {
            f'{user_name}': {
                'password': password,
                'email': email
            }
        }
        client.emit('add_user', user_data)
        termcolor.cprint('Account successfully created.',
                         'green', attrs=['bold'])
        start()

    else:
        # do pass to menu. ye tabeh tarif kon baraye back to manu
        start()


def is_user_name_valid(user_name):
    client.emit('user_name_validity', user_name)


@client.on('is_user_name_valid_resp')
def is_user_name_valid_resp(user_name_validity_answer):
    global check_user_name
    global is_check_user_name_done
    if not user_name_validity_answer:
        termcolor.colored(
            '''Sorry \U0001F927. Your user name is invalid.''', 'yellow', attrs=['bold'])
        check_user_name = False
        is_check_user_name_done = True
    else:
        check_user_name = True
        is_check_user_name_done = True


def login():
    termcolor.cprint('''Welcome to login page \U0001F603 ''',
                     'cyan', attrs=['bold'])
    user_name = input(termcolor.colored('User Name: ', 'cyan', attrs=['bold']))
    password = getpass(termcolor.colored('Password: ', 'cyan', attrs=['bold']))
    password = pbkdf2_hash(password)
    password = {'password': password}  # creating dict
    login_info = {}
    login_info[user_name] = password
    client.emit('ckeck_login_info', login_info,
                callback=check_login_resp)


@ client.on('check_login_resp')
def check_login_resp(response):
    if response:
        termcolor.cprint('Wait for the second player...',
                         'yellow', attrs=['bold'])
        start_new_game()
        return True
    termcolor.cprint('Incorrect login info! Try again.',
                     'yellow', attrs=['bold'])
    login()


def request_leader_board():
    client.emit('give_leader_board')


@ client.on('get_leader_board')
def get_leader_board(leader_board):
    print(leader_board)

    back_to_menu = input(termcolor.colored(
        'Enter any key to back to menu: ', 'yellow', attrs=['bold']))

    start()


@client.on('get_rtbf_resp')
def get_rtbf_resp(rtbf_resp):
    if rtbf_resp:
        termcolor.cprint(
            'Account successfully deleted! BYE \U0001F590', 'green', attrs=['bold'])
    else:
        termcolor.cprint('Invalid account info!', 'yellow', attrs=['bold'])

    start()


def start():  # aval bazi in namayesh dadeh mishe ke user chikar mikhad kone
    Login_ = termcolor.colored('2) Leader board (enter 2)',
                               'magenta', attrs=['bold'])
    Sign_up_ = termcolor.colored(
        '3) sign-up (enter 3)', 'yellow', attrs=['bold'])
    Help_page_ = termcolor.colored(
        '4) See "what is game about?" (enter 4)', 'green', attrs=['bold'])

    About_me_ = termcolor.colored(
        '5) About me (game creator) (enter 5)', 'blue', attrs=['bold'])

    Delete_account_ = termcolor.colored(
        '6) Delete account (Right To Be Forgotten) (enter 6)', 'green', attrs=['bold'])

    Privacy_policy_ = termcolor.colored(
        '7) Privacy Policy (enter 7)', 'yellow', attrs=['bold'])

    operation = input(termcolor.colored(f'''Hi \U0001F64B
        What do you want to do?
        1) Login (enter 1)
        {Login_}
        {Sign_up_}
        {Help_page_}
        {About_me_}
        {Delete_account_}
        {Privacy_policy_}
        ''', 'cyan', attrs=['bold']))

    if operation == '1':
        login()

    elif operation == '2':
        request_leader_board()

    elif operation == '3':
        user_data = sign_up()

    elif operation == '4':
        game_help_page()
        start()

    elif operation == '5':
        about_game_creator()
        back_to_menu = input(termcolor.colored(
            'Enter any key to back to meny: ', 'cyan', attrs=['bold']))
        start()

    elif operation == '6':
        rtbf()

        user_name = input(termcolor.colored(
            'User Name: ', 'cyan', attrs=['bold']))
        password = getpass(termcolor.colored(
            'Password: ', 'cyan', attrs=['bold']))
        password = pbkdf2_hash(password)
        password = {'password': password}  # creating dict
        account_info = {}
        account_info[user_name] = password
        client.emit('get_rtbf_req', account_info)

    elif operation == '7':
        privacy_policy_text()
        start()

    else:
        termcolor.cprint(
            '''Sorry. you wrote something that is invalid.
            please enter "1" or "2" or "3" or "4" or "5" or "6" or "7" ''', 'yellow', attrs=['bold'])
        start()


# ------------------------------------------------------
def start_new_game():
    client.emit('give_ready_players', '1')


@client.on('can_i_join')
def can_i_join(can_i):
    if can_i == False:
        termcolor.cprint(
            'Oh, server is busy. please try again later ', 'yellow', attrs=['bold'])
        start()

    else:
        termcolor.cprint('Good! Wait for second player! ',
                         'green', attrs=['bold'])


@client.on('choose_piece')
def choose_piece(pieces):
    choosed_piece = input(termcolor.colored(
        f'pick a piece from {pieces}: \n', 'cyan', attrs=['bold']))

    while choosed_piece not in pieces:  # avoid invalid input
        termcolor.cprint(
            'Sorry. you shoud choose between those I gave you!', 'yellow', attrs=['bold'])
        choosed_piece = input(termcolor.colored(
            f'pick a piece from {pieces}: \n', 'cyan', attrs=['bold']))

    client.emit('get_choosen_piece', choosed_piece)


@client.on('choose_move')
def choose_move(choosed_piece_to_move_data):  # agar bishtar az 16 dad
    move = input(termcolor.colored(
        f'move {choosed_piece_to_move_data[0]} to which square?: ', 'cyan', attrs=['bold']))
    numbers_can_choose = choosed_piece_to_move_data[1]

    while move not in numbers_can_choose:
        termcolor.cprint('Invalid input.', 'yellow', attrs=['bold'])
        move = input(termcolor.colored(
            f'move {choosed_piece_to_move_data[0]} to which square?: ', 'cyan', attrs=['bold']))

    client.emit('get_choosen_move', int(move))


@client.on('get_board')
def get_board(board):
    print()
    print(board)


@client.on('i_won')
def i_won(won_text):
    termcolor.cprint(won_text+'\n', 'green', attrs=['bold'])
    back_to_menu = input(termcolor.colored(
        'Enter any key to back to menu: ', 'cyan', attrs=['bold']))
    start()


@client.on('i_lost')
def i_lost(lost_text):
    termcolor.cprint(lost_text+'\n', 'yellow', attrs=['bold'])
    back_to_menu = input(termcolor.colored(
        'Enter any key to back to menu\n', 'cyan', attrs=['bold']))
    start()


@client.on('tie')
def tie():
    termcolor.cprint('Tie!')
    back_to_menu = input(termcolor.colored(
        'Enter any key to back to menu \U0001F971 \n', 'cyan', attrs=['bold']))
    start()


# -----------------------------------
client.connect("http://127.0.0.1:5000")
first_time = False
start()
first_time = True
