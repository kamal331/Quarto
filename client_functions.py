import termcolor
import os
import binascii
from backports.pbkdf2 import pbkdf2_hmac


def sign_up_message():
    termcolor.cprint('READ THIS:', 'red', 'on_white')
    Warning_ = termcolor.colored(
        'Warning', 'magenta', 'on_yellow', attrs=['underline'])
    Greate_pass_ = termcolor.colored('DLy$Bds2}bS!7Mis^d1AdV7%pSBrQ@', 'cyan')
    termcolor.cprint('READ THIS:', 'red', 'on_white')
    print()
    termcolor.cprint('Your data, your rights\U0001F60A.',
                     'cyan', 'on_grey', ['bold', 'underline'])
    print()
    print(f'''1) We value your privacy. We do NOT collect any kind of personal data
    your e-mail is a kind of personal data. So your are not obliged to
    enter your e-mail address. If you enter your email address you can
    recover your account if you forgot your password. So if you don't
    provide your e-mail address make sure you write your password and
    store it in safe place.
    {Warning_}: if you lost your password and you didn't provide your e-mail
    address, there is NO way to recover your account as we store your
    password in hash type. \n
    2) we don't store your password in plain text. I use "PBKDF2" hash
    algorithm which is recommended by "NIST" (National Institute of
    Standards and Technology)   ---> NIST Special Publication SP800-63B-3\n
    3) We do Not get any other data. because it's not our business.
    Your age, your name, your last name, etc... are all your business.\n
    4) make sure to choose a strong password. It means your password must
    include Capital letter (A-Z) + Small letter (a-z) + numbers(0-9) +
    symbols ( !@#$%^&*()-}}{{? ). And make sure that it has atleast 15 character
    Example of a great password: {Greate_pass_}\n
    5) Your user name must not include symbols (Except "_") and it must
    be at least 4 character. If you are confident that you entered valid user name,
    and you cannot sign-up, it's because your choosen user name is same as
    another person's user name. So you must pick another thing!''')


def game_help_page():
    wikipedia_website_for_game_info = termcolor.colored(
        'https://en.wikipedia.org/wiki/Quarto_(board_game)', 'yellow')
    termcolor.cprint(
        f'This text is from wikipedia ---> {wikipedia_website_for_game_info}', 'magenta')
    termcolor.cprint('''
    Quarto is a board game for two players invented by Swiss mathematician Blaise Müller.[1]
    It is published and copyrighted by Gigamic.

    The game is played on a 4×4 board.[2][3] There are 16 unique pieces to play with, each of which is either:

        - tall or short;
        - red or blue (or a different pair of colors, e.g. light- or dark-stained wood);
        - square or circular; and
        - hollow-top or solid-top.

    Players take turns choosing a piece which the other player must then place on the board. 
    A player wins by placing a piece on the board which forms a horizontal, vertical, or diagonal row of
    four pieces, all of which have a common attribute (all short, all circular, etc.).''', 'cyan')

    back_to_menu_from_help_page = input(
        termcolor.colored('Enter any key to back to menu: '))


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


def pbkdf2_hash(password):
    salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
    passwd = f"{password}".encode("utf8")
    key = pbkdf2_hmac("sha256", passwd, salt, 50000, 32)
    return binascii.hexlify(key)


def email_validity(email):
    for char in email:
        if char in ''' !#$%^&*()-=+`~|}]{['"?/\<:;,''':
            return False

    if ('@' in email and '.' in email) or (email == '0'):
        return True

    return False
