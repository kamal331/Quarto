from argon2 import PasswordHasher, Type
from socketio import *

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


def resp(response):
    print(response)


def start_game_resp(response):
    print(response)


def confirm_pass(password, confirm_password):
    return password == confirm_password


def argon2_hash(password):
    ph = PasswordHasher(
        memory_cost=65536,
        time_cost=400,
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )

    passwordHash = ph.hash(password)

    return passwordHash


def sign_up():
    print('''READ THIS:\n
    Your data, your right.\n
    1) We value your privacy. We do NOT collect any kind of personal data
    your e-mail is a kind of personal data. So your are not obliged to 
    enter your e-mail address. If you enter your email address you can
    recover your account if you forgot your password. So if you don't 
    provide your e-mail address make sure you write your password and
    store it in safe place.\n
    Warning: if you lost your password and you didn't provide your e-mail
    address, there is NO way to recover your account as we store your
    password in hash type
    2) we don't store your password in plain text. I use "Argon2" algorithm
    which is one of the best options available for hishign. The only con is 
    slow. But your security is important your should choose security over speed.
    So if it takes like 20 second, don't worry. Because this hash algorithm is 
    slow!
    3) We do Not get any other data. because it's not our business. 
    Your age, your name, your last name, etc... are all your business. 
    ''')
    user_name = input('User Name: ')
    password = input('Password: ')
    confirm_password = input('enter your password again: ')

    while confirm_pass(password, confirm_password):
        print('Sorry \U0001F613 second password you entered, doesn\'t match with first password')
        confirm_password = input('enter your password again: ')
    email = input(
        '''e-mail: (optional. You do NOT oblidge to enter your e-mail address)
        if you Don,t want, just enter "0" ''')
    confirm = input(
        'Do you want to sign-up? write "yes". If you don\'t, write "no" to back to the menu').lower()
    if confirm == 'yes':
        pass
    else:
        # do pass to menu. ye tabeh tarif kon baraye back to manu
        pass
    user_data = {
        'user_name': user_name,
        'password': password,
        'email': email
    }
    return user_data


def login():
    user_name = input('User Name:')
    password = input('Password:')
    password = argon2_hash(password)  # hashing it


loggin_info = {'user_name': user_name, 'age': age}

client.emit('welcome', data=loggin_info, callback=resp)

name = input('enter name: ')
result = {'user1': user_name, 'user2': name}


client.emit('start_game', mdata=loggin_info, callback=resp)
