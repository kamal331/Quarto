import termcolor
import os
import binascii
from backports.pbkdf2 import pbkdf2_hmac


# ------------------------ Sign Up ------------------------

def sign_up_message():
    Warning_ = termcolor.colored(
        'Warning', 'magenta', attrs=['underline', 'bold'])
    Greate_pass_ = termcolor.colored('DLy$Bds2}bS!7Mis^d1AdV7%pSBrQ@', 'cyan')
    Number_1_ = termcolor.colored('1)', 'magenta', attrs=['bold'])
    Number_2_ = termcolor.colored('2)', 'magenta', attrs=['bold'])
    Number_3_ = termcolor.colored('3)', 'magenta', attrs=['bold'])
    Number_4_ = termcolor.colored('4)', 'magenta', attrs=['bold'])
    Number_5_ = termcolor.colored('5)', 'magenta', attrs=['bold'])
    Pbkdf2_ = termcolor.colored('"PBKDF2"', 'cyan', attrs=['bold'])
    Nist_ = termcolor.colored('"NIST"', 'cyan', attrs=['bold'])
    Plus_sign_ = termcolor.colored('+', 'yellow', attrs=['bold'])
    Symbols_ = termcolor.colored('!@#$%^&*()-}{?', 'cyan', attrs=['bold'])
    termcolor.cprint('READ THIS:', 'red', 'on_white')
    print()
    termcolor.cprint('Your data, your rights\U0001F60A.',
                     'cyan', 'on_grey', ['bold', 'underline'])
    print()
    print(f'''{Number_1_} We value your privacy. We do NOT collect any kind of personal data
    your e-mail is a kind of personal data. So your are not obliged to
    enter your e-mail address. If you enter your email address you can
    recover your account if you forgot your password. So if you don't
    provide your e-mail address make sure you write your password and
    store it in safe place.
    {Warning_}: if you lost your password and you didn't provide your e-mail
    address, there is NO way to recover your account as we store your
    password in hash type. \n
{Number_2_} we don't store your password in plain text. I use {Pbkdf2_} hash
    algorithm which is recommended by {Nist_} (National Institute of
    Standards and Technology)   ---> NIST Special Publication SP800-63B-3\n
{Number_3_} We do Not get any other data. because it's not our business.
    Your age, your name, your last name, etc... are all your business.\n
{Number_4_} make sure to choose a strong password. It means your password must
    include Capital letter (A-Z) {Plus_sign_} Small letter (a-z) {Plus_sign_} numbers(0-9) {Plus_sign_}
    symbols ( {Symbols_} ). And make sure that it has atleast 15 character
    Example of a great password: {Greate_pass_}\n
{Number_5_} Your user name must not include symbols (Except "_") and it must
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
    termcolor.cprint('''I use Blue and Yellow collor. here are pieces. Also you can see those at real-time
    you're playing. NOTE: board squares is numbered from top left.
    ''', 'yellow', attrs=['bold'])
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
    # DONT !!!! Forget to do .lower()
    pointer_sign = termcolor.colored('--->', 'magenta')
    termcolor.cprint(f'''
    \U0001F7E6  {pointer_sign} Big Blue Solid-top Square {Left_parantesis_}bbss{Right_parantesis_}
    \U0001F7E8  {pointer_sign} Big Yellow Solid-top Sqaure {Left_parantesis_}byss{Right_parantesis_}
    {Little_blue_solid_square_}   {pointer_sign} small Blue Solid-top Square {Left_parantesis_}sbss{Right_parantesis_}
    {Little_yellow_solid_square_ }   {pointer_sign} Small Yellow Solid-top Sqaure {Left_parantesis_}syss{Right_parantesis_}
    {Big_blue_hallowtop_square_}   {pointer_sign} Big Blue Hallow-top square {Left_parantesis_}bbhs{Right_parantesis_}
    {Big_yellow_hallowtop_square_}   {pointer_sign} Big Yellow Hallow-top Square {Left_parantesis_}byhs{Right_parantesis_}
    {Small_blue_hallowtop_square_}   {pointer_sign} Small Blue Hallow-top square {Left_parantesis_}sbhs{Right_parantesis_}
    {Small_yellow_hallowtop_square_}   {pointer_sign} Small Yellow Hallow-top square {Left_parantesis_}syhs{Right_parantesis_}
    \U0001F535  {pointer_sign} Big Blue Solid-top Circle {Left_parantesis_}bbsc{Right_parantesis_}
    \U0001F7E1  {pointer_sign} Big Yellow Solid-top Circle {Left_parantesis_}bysc{Right_parantesis_}
    {Small_blue_little_circle_}   {pointer_sign} Small Blue Solid-top Circle {Left_parantesis_}sbsc{Right_parantesis_}
    {Small_yellow_little_circle_}   {pointer_sign} Small Yellow Solid-top Circle {Left_parantesis_}sysc{Right_parantesis_}
    {Big_blue_hallowtop_circle_}   {pointer_sign} Big Blue Hallowtop Circle {Left_parantesis_}bbhc{Right_parantesis_}
    {Big_yellow_hallowtop_circle_}   {pointer_sign} Big Yellow Hallowtop Circle {Left_parantesis_}byhc{Right_parantesis_}
    {Small_blue_hallowtop_circle_}   {pointer_sign} Small Blue Hallowtop Circle {Left_parantesis_}sbhc{Right_parantesis_}
    {Small_yellow_hallowtop_circle_}   {pointer_sign} Small Yellow Hallowtop Circle {Left_parantesis_}syhc{Right_parantesis_}
    ''', 'yellow')
    back_to_menu_from_help_page = input(
        termcolor.colored('Enter any key to back to menu: ', 'cyan', attrs=['bold']))


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


def confirm_pass(password, confirm_password):
    return password == confirm_password


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


# ------------------------ About game creator ------------------------

def some_talk_text():
    Read_these_ = termcolor.colored('Read these:', 'red', 'on_white')
    I_LOVE_YOU_ = termcolor.colored(
        '"I LOVE YOU"', 'yellow', attrs=['bold'])
    Say_ = termcolor.colored('say', 'cyan')
    Number5_text_ = termcolor.colored('''
        or any other verbal affections to those you love.
        Life is really short. Nobody knows if he/she is alive tomorrow or not.
        Love those you love, like this is the last day of your life.
    
    Buh-bye \U0001F33F \U0001F339''', 'cyan', attrs=['bold'])
    termcolor.cprint(f'''Hey. I hope you\'re feeling good.
    BTW I know it's a bit strange to see these in a game, but please 
    {Read_these_}
    
    1) Love yourself! But don't be selfish.''', 'blue', attrs=['bold'])

    termcolor.cprint('''
    2) Have fun! But don't waste your time in games. I know that you know your
        time is so important. Make a balance for your work and your fun. (OR you
        can choose a job that is fun for you and you love it. Some parents say
        You must be ... in the future. But if you don't like that job
        and you probably will hate it, please don't choose it. let's think you want
        to be a doctor and you don't like it. So it's not a patient's right that you
        treat him with bad morals!!
        - No. I am a kind person. )
        + OK. But Every time you wake up, you're angry that you have to go to work.
        The work that you don't like it (Or you hate it.)
        BECAREFUL! Money is not everything but if you don't have money,
        you can't live without it make sure you can get enough money for living in 
        that job which you like.''', 'green', attrs=['bold'])

    termcolor.cprint('''
    3) You're valuable. Don't lower your value by treating yourself inhumanely,
        mistreating others and oppressing the rights of others.''', 'magenta', attrs=['bold'])

    termcolor.cprint('''
    4) Teach others knowledge. Defend the rights of good people. 
        I promise you that you get answers to your good deeds one day.
        The world needs more good people. Please be one of them.''', 'yellow', attrs=['bold'])

    termcolor.cprint(
        f'''
    5) {Say_} {I_LOVE_YOU_} {Number5_text_}
    ''', 'cyan', attrs=['bold'])


# ------------------------ RTBF ------------------------

def rtbf():

    wikipedia_website_for_rtbf = termcolor.colored(
        'https://en.wikipedia.org/wiki/Right_to_be_forgotten', 'yellow')
    termcolor.cprint(
        f'This text is from wikipedia ---> {wikipedia_website_for_rtbf}', 'magenta')

    termcolor.cprint('''
    The right to be forgotten (RTBF[1]) is the right to have private information
    about a person be removed from Internet searches and other directories under
    some circumstances. The concept has been discussed and put into practice in
    several jurisdictions, including Argentina,[2][3] European Union (EU), 
    and the Philippines.
    ''', 'cyan')

    termcolor.cprint('''
    We respect your privacy. So you can simply delete your account.
    You must enter your User name, Password.
    ''')


# ------------------------ Privacy Policy ------------------------

def privacy_policy_text():
    termcolor.cprint('''
    I (means game creator) am serious about your privacy Because it is your "right".
    I put privacy at first.
    
    What I collect?

    1) User Name: your user name is public.
    
    2) Wins, Lossess and Ties: Your Wins, Lossess, Ties are public.
    
    3) E-mail: your e-mail address is stored to my server. (email address is optional. And is NOT required.
    because it is your privacy.)
    
    4) Hashed password: Your password is Hashed with PBKDF2 hash algorithm which is recommended by
    NIST (National Institute of Standards and Technology)   ---> NIST Special Publication SP800-63B-3
    
    5) ID: it is a random string and everytime you connect to server, it will be a different thing. 

    6) When you transfer data to my server, this is happenning in server:
    127.0.0.1 (IP) - - [2022-01-20 12:08:24] "GET /socket.io/?transport=polling&EIO=4&sid=LoYaykW4wtehfdkAAAA&t=1642652533.6654613 HTTP/1.1" 200 157 0.931671
    I don't record it. But this prints in server. If you know how to remove this, I will be happy if you tell me.
    
    Nothing else \U0001F60A
    
    NOTE: You can always delete your account. (It is your right to be forgotten)

    ''', 'cyan', attrs=['bold'])

    back_to_menu = input(termcolor.colored(
        'Enter any key to back to menu: ', 'cyan', attrs=['bold']))
