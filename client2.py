from argon2 import PasswordHasher, Type
from socketio import *
from getpass import getpass

client = Client()
client.connect("http://127.0.0.1:5000")


@client.event
def connect():
    print("I'm connected")


@client.event
def connect_error(data):
    print('Connection failed')


@client.event()
def disconnect():
    print("I'm disconnected")


def start_game_resp(response):
    print(response)


def confirm_pass(password, confirm_password):
    return password == confirm_password


def argon2_hash(password):
    ph = PasswordHasher(
        memory_cost=65000,  # 256000
        time_cost=4,  # 400
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )

    passwordHash = ph.hash(password)

    return passwordHash


check_user_name = False


def sign_up():
    global check_user_name
    print('''READ THIS:\n
    Your data, your right\U0001F60A.\n
    1) We value your privacy. We do NOT collect any kind of personal data
    your e-mail is a kind of personal data. So your are not obliged to 
    enter your e-mail address. If you enter your email address you can
    recover your account if you forgot your password. So if you don't 
    provide your e-mail address make sure you write your password and
    store it in safe place.
    Warning: if you lost your password and you didn't provide your e-mail
    address, there is NO way to recover your account as we store your
    password in hash type. \n
    2) we don't store your password in plain text. I use "Argon2" algorithm
    which is one of the best options available for hishign. The only con is 
    slow. But your security is important your should choose security over speed.
    So if it takes like 20 second, don't worry. Because this hash algorithm is 
    slow!\n
    3) We do Not get any other data. because it's not our business. 
    Your age, your name, your last name, etc... are all your business.\n
    4) make sure to choose a strong password. It means your password must
    include Capital letter (A-Z) + Small letter (a-z) + numbers(0-9) + 
    symbols ( !@#$%^&*()-}{? ). And make sure that it has atleast 15 character
    Example of a great password: DLy$Bds2}bS!7Mis^d1AdV7%pSBrQ@\n
    5) Your user name must not include symbols (Except "_") and it must
    be at least 4 character. If you are confident that you entered valid user name,
    and you cannot sign-up, it's because your choosen user name is same as
    another person's user name. So you must pick another thing!
    ''')
    user_name = 'a'
    is_user_name_valid(user_name='a')
    #user_name = input('User Name: ')
    while not check_user_name:
        a = 1
    password = getpass()  # getting hiden pass for security
    while not is_pass_Strong(password):
        print(('your password is not strong enough'))
        password = getpass()

    print('enter your password again')
    confirm_password = getpass()

    while not confirm_pass(password, confirm_password):
        print('Sorry \U0001F613. second password you entered, doesn\'t match with first password')
        confirm_password = input('enter your password again: ')

    email = input(
        '''E-mail: (optional. You do NOT oblidge to enter your e-mail address)
        if you Don,t want, just enter "0": ''')
    while not email_validity(email):
        print('your e-mail is not valid. eneter another one.')
        email = input('E-mail: ')

    confirm = input(
        'Do you want to sign-up? write "yes". If you don\'t, write "no" to back to the menu: ').lower()
    if confirm == 'yes':
        pass
    else:
        # do pass to menu. ye tabeh tarif kon baraye back to manu
        pass

    # we don't pass hashed password to server!
    password = argon2_hash(password)
    user_data = {
        f'{user_name}': {
            'password': password,
            'email': email}
    }
    return user_data
    # user_data = {
    #    'user_name': user_name,
    #    'password': password,
    #    'email': email
    # }
    # return user_data


def is_user_name_valid(user_name):
    user_name = input('User Name: ')
    client.emit('user_name_validity', user_name, callback=resp)
    # print('''Sorry this user name has been given to another player \U0001F61E.
    # Try another one''')


def resp(response):
    global check_user_name
    check_user_name = False
    if not response:
        print('''Your user name must not include symbols (Except "_") and it must
    be at least 4 character. If you are confident that you entered valid user name,
    and you cannot sign-up, it's because your choosen user name is same as
    another person's user name. So you must pick another thing!''')
        is_user_name_valid(user_name='a')
    check_user_name = True


def is_pass_Strong(password):
    up = 0
    low = 0
    num = 0
    symb = 0
    if len(password) < 15:  # password lenght must be 15 or more character
        return False

    for char in password:
        if char.isupper():
            up += 1

        elif char.islower():
            low += 1

        elif char.isnumeric():
            num += 1

        else:
            symb += 1

    if up >= 3 and low >= 3 and symb >= 3 and num >= 3:
        return True

    return False


def email_validity(email):
    if ('@' in email and '.' in email) or (email == '0'):
        return True
    return False


def login():
    user_name = input('User Name:')
    password = getpass()
    password = argon2_hash(password)  # hashing it
    login_info = {}
    login_info[user_name] = password


operation = input(''' What do you want to do?
1) Login (enter 1)
2) Leader board (enter 2)
3) sign-up (enter 3)
''')  # aval bazi in namayesh dadeh mishe ke user chikar mikhad kone

if operation == '1':
    login()

elif operation == '2':
    # leader() ezafe kon
    pass

elif operation == '3':
    user_data = sign_up()

client.emit('add_user', user_data)

# loggin_info = {'user_name': user_name, 'age': age}

#client.emit('welcome', data=loggin_info, callback=resp)

# name = input('enter name: ')
#result = {'user1': user_name, 'user2': name}


#client.emit('start_game', mdata=loggin_info, callback=resp)
"""
user_name = input('User Name: ')
    
    while not is_user_name_valid(user_name):
        user_name = input('User Name: ')
"""
