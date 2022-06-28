import os
import sys
os.system("cls")
print("""
███    ██ ███████ ████████ ███████ ██      ██ ██   ██ 
████   ██ ██         ██    ██      ██      ██  ██ ██  
██ ██  ██ █████      ██    █████   ██      ██   ███   
██  ██ ██ ██         ██    ██      ██      ██  ██ ██  
██   ████ ███████    ██    ██      ███████ ██ ██   ██ 
""")

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
if sys.version_info[0] < 3:
    print("Please download Python3 from the link below")
    print("https://www.python.org/downloads/")
    input("Press any key to exit!")
    sys.exit("Python3 not installed")

try:
    os.system("pip3 install -q --disable-pip-version-check --no-cache-dir --no-color --no-warn-conflicts mysql-connector-python")
    os.system("pip3 install -q --disable-pip-version-check --no-cache-dir --no-color --no-warn-conflicts ipinfo")
    os.system("pip3 install -q --disable-pip-version-check --no-cache-dir --no-color --no-warn-conflicts datetime")
    os.system("pip3 install -U -q --disable-pip-version-check --no-cache-dir --no-color --no-warn-conflicts cffi pip setuptools")
    os.system("pip3 install -q --disable-pip-version-check --no-cache-dir --no-color --no-warn-conflicts argon2-cffi")
    os.system("pip3 install -q --disable-pip-version-check --no-cache-dir --no-color --no-warn-conflicts termcolor")
    os.system("pip3 install -q --disable-pip-version-check --no-cache-dir --no-color --no-warn-conflicts lxml")
except:
    sys.exit("Unable to install required dependencies!")

try:
    import argon2
    import ipinfo
    import datetime
    import time
    import termcolor
    import base64
    import imaplib
    import json
    import smtplib
    import urllib.parse
    import urllib.request
    import lxml
    import random
    from getpass import getpass
    from mysql.connector import connect
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from lxml import html

except:
    sys.exit("Unable to import required dependencies")


ip_details = ipinfo.getHandler("eb85c6b947bbc4").getDetails()

cdb = connect(host="localhost", user="root", password="17102005")
db = cdb.cursor()
db.execute("CREATE DATABASE IF NOT EXISTS netflix")
cdb.commit()
db.close()
cdb.close()

cdb = connect(host="localhost", user="root", password="17102005", database="netflix")
db = cdb.cursor()

db.execute("CREATE TABLE IF NOT EXISTS content(netflix_id BIGINT PRIMARY KEY NOT NULL, title LONGTEXT NOT NULL, type VARCHAR(10) NOT NULL, rating VARCHAR(15) NOT NULL, release_year YEAR NOT NULL, actor1 CHAR(5) NOT NULL, actor2 CHAR(5) NOT NULL, actor3 CHAR(5) NOT NULL, actor4 CHAR(5) NOT NULL, director CHAR(5) NOT NULL, category VARCHAR(255) NOT NULL, imdb VARCHAR(20) NOT NULL, runtime VARCHAR(50) NOT NULL, description LONGTEXT NOT NULL, language VARCHAR(255) NOT NULL, price FLOAT NOT NULL, VAT FLOAT NOT NULL DEFAULT 5.0)")
db.execute("CREATE TABLE IF NOT EXISTS actors(id CHAR(5) PRIMARY KEY NOT NULL, name LONGTEXT)")
db.execute("CREATE TABLE IF NOT EXISTS directors(id CHAR(5) PRIMARY KEY NOT NULL, name LONGTEXT)")
db.execute("CREATE TABLE IF NOT EXISTS customers(name LONGTEXT NOT NULL, email LONGTEXT NOT NULL, phone_number LONGTEXT NOT NULL, username LONGTEXT NOT NULL, country_Code CHAR(3) NOT NULL, balance FLOAT NOT NULL DEFAULT 0.0, PRIMARY KEY index_username(username(100)))")
db.execute("CREATE TABLE IF NOT EXISTS auth(username LONGTEXT NOT NULL, passhash LONGTEXT NOT NULL, PRIMARY KEY index_username(username(100)))")
db.execute("CREATE TABLE IF NOT EXISTS orders(id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL, customer_ID BIGINT NOT NULL, date DATETIME)")
db.execute("CREATE TABLE IF NOT EXISTS order_details(order_iD BIGINT NOT NULL, content_id BIGINT NOT NULL, amount BIGINT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS cart(username LONGTEXT, netflix_id BIGINT NOT NULL, title LONGTEXT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS sudo_logs(query LONGTEXT, query_timestamp LONGTEXT)")
db.execute("CREATE TABLE IF NOT EXISTS admin(username LONGTEXT NOT NULL, passhash LONGTEXT NOT NULL, PRIMARY KEY index_username(username(100)))")

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

GOOGLE_CLIENT_ID = '883495880858-pa24r44unorsao9if8gsvbcqrr2j44bc.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REFRESH_TOKEN = '1//031ss_eVdJF8XCgYIARAAGAMSNwF-L9Ircikq_lAO5vUoc5FiQJnFYi4L7-6ZeZ2F-ZfW476Iu-K1KCx-tkFbpeYaMVf1RXFAckc'

login_status = False

actors = {}
db.execute("SELECT * FROM actors")
for i in db.fetchall():
    key = i[0]
    value = i[1]
    actors.update({key: value})

directors = {}
db.execute("SELECT * FROM directors")
for i in db.fetchall():
    key = i[0]
    value = i[1]
    directors.update({key: value})


# EMAIL DEFINITION START
def command_to_url(command):
    return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)


def url_escape(text):
    return urllib.parse.quote(text, safe='~-._')


def url_unescape(text):
    return urllib.parse.unquote(text)


def url_format_params(params):
    param_fragments = []
    for param in sorted(params.items(), key=lambda x: x[0]):
        param_fragments.append('%s=%s' % (param[0], url_escape(param[1])))
    return '&'.join(param_fragments)


def generate_permission_url(client_id, scope='https://mail.google.com/'):
    params = {}
    params['client_id'] = client_id
    params['redirect_uri'] = REDIRECT_URI
    params['scope'] = scope
    params['response_type'] = 'code'
    return '%s?%s' % (command_to_url('o/oauth2/auth'), url_format_params(params))


def call_authorize_tokens(client_id, client_secret, authorization_code):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['code'] = authorization_code
    params['redirect_uri'] = REDIRECT_URI
    params['grant_type'] = 'authorization_code'
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def call_refresh_token(client_id, client_secret, refresh_token):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['refresh_token'] = refresh_token
    params['grant_type'] = 'refresh_token'
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)


def generate_oauth2_string(username, access_token, as_base64=False):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if as_base64:
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    return auth_string


def test_imap(user, auth_string):
    imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_conn.debug = 4
    imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    imap_conn.select('INBOX')


def test_smpt(user, base64_auth_string):
    smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_conn.set_debuglevel(True)
    smtp_conn.ehlo('test')
    smtp_conn.starttls()
    smtp_conn.docmd('AUTH', 'XOAUTH2 ' + base64_auth_string)


def get_authorization(google_client_id, google_client_secret):
    scope = "https://mail.google.com/"
    print('Navigate to the following URL to auth:', generate_permission_url(google_client_id, scope))
    authorization_code = input('Enter verification code: ')
    response = call_authorize_tokens(google_client_id, google_client_secret, authorization_code)
    return response['refresh_token'], response['access_token'], response['expires_in']


def refresh_authorization(google_client_id, google_client_secret, refresh_token):
    response = call_refresh_token(google_client_id, google_client_secret, refresh_token)
    return response['access_token'], response['expires_in']


def send_mail(fromaddr, toaddr, subject, message):
    access_token, expires_in = refresh_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)
    auth_string = generate_oauth2_string(fromaddr, access_token, as_base64=True)

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg.preamble = 'This is a multi-part message in MIME format.'
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    part_text = MIMEText(lxml.html.fromstring(message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
    part_html = MIMEText(message.encode('utf-8'), 'html', _charset='utf-8')
    msg_alternative.attach(part_text)
    msg_alternative.attach(part_html)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo(GOOGLE_CLIENT_ID)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

# EMAIL DEFINITION END


def record_checker(tablename, fieldname, variable):
    db.execute("SELECT {mycolumn} FROM {mytablename}".format(mycolumn=fieldname, mytablename=tablename), ())
    if variable not in db.fetchall():
        print("Does not exist!")
        return False

    else:
        return True


def pass_hasher(password):
    return argon2.PasswordHasher().hash(password)


def pass_verify(hash, inputpass):
    return argon2.PasswordHasher().verify(hash, inputpass)


def gen_otp():
    return str(int(random.random()*1000000))


def add_content():
    netflix_id = int(input("Enter Netflix ID: "))
    title = input("Enter content title: ")
    print("Content types:")
    print("1. Movie")
    print("2. TV Show")
    c = int(input("Select content type:"))
    if c == 1:
        type = "Movie"
    elif c == 2:
        type = "TV Show"
    else:
        sys.exit("Invalid content type")
    rating = input("Enter PG rating: ")
    release_year = int(input("Enter release year: "))
    actor1 = input("Enter actor1 code:")
    actor2 = input("Enter actor2 code (use AC000 for NULL): ")
    actor3 = input("Enter actor3 code (use AC000 for NULL): ")
    actor4 = input("Enter actor4 code (use AC000 for NULL): ")
    rc1 = record_checker("actors", 'id', actor1)
    rc2 = record_checker("actors", 'id', actor2)
    rc3 = record_checker("actors", 'id', actor3)
    rc4 = record_checker("actors", 'id', actor4)
    director = input("Enter director code: ")
    rc5 = record_checker("directors", 'id', director)
    category = input("Enter content category: ")
    imdb = input("Enter IMDB rating: ")
    runtime = int(input("Enter content length in minutes: "))
    runtime += "min"
    description = input("Enter content description: ")
    language = input("Enter content language: ")
    price = float(input("Enter content price: "))
    vat = float(input("Enter content VAT: "))
    db.execute("INSERT INTO content(netflix_id, title, type, rating, release_year, actor1, actor2, actor3, actor4, director, category, imdb, runtime, description, language, price, vat)  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (netflix_id, title, type, rating, release_year, actor1, actor2, actor3, actor4, director, category, imdb, runtime, description, language, price, vat)) if rc1 == True and rc2 == True and rc3 == True and rc4 == True and rc5 == True else print("Record not added!")
    cdb.commit()


def add_actor():
    id = input("Enter actor ID: ")
    name = input("Enter actor's full name: ")
    db.execute("INSERT INTO actors VALUES(%s, %s)", (id, name))
    cdb.commit()


def add_director():
    id = input("Enter director ID: ")
    name = input("Enter director's full name: ")
    db.execute("INSERT INTO directors VALUES(%s, %s)", (id, name))
    cdb.commit()


def register_customer():
    name = input("Enter your Full Name: ")
    email = input("Enter your email: ")
    phone_number = input("Enter your phone number in international format: ")
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    passhash = pass_hasher(password)
    db.execute("INSERT INTO customers (name, email, phone_number, username, country_code) VALUES(%s, %s, %s, %s, %s)",
               (name, email, phone_number, username, ip_details.country))
    cdb.commit()
    db.execute("INSERT INTO auth VALUES(%s, %s)", (username, passhash))
    cdb.commit()
    os.system("cls")
    print("You have successfully registered! Please run the program again and login!")
    sys.exit(0)


def edit_actor():
    acn = input("Enter actor ID: ")
    db.execute("SELECT name FROM actors WHERE id = %s", (acn,))
    print("Actor name: ", db.fetchall()[0][0])
    new = input("Enter new actor name: ")
    db.execute("UPDATE actors SET name = %s WHERE id = %s", (new, acn)) if acn else print("Actor editing failed!")
    cdb.commit()
    print("Actor successfully edited")


def edit_director():
    drn = input("Enter director ID: ")
    db.execute("SELECT name FROM directors WHERE id = %s", (drn,))
    print("Director name: ", db.fetchall()[0][0])
    new = input("Enter new director name: ")
    db.execute("UPDATE directors SET name = %s WHERE id = %s", (new, drn)) if drn else print("Director editing failed!")
    cdb.commit()
    print("Director successfully edited")


def edit_content():
    nid = input("Enter Netflix ID: ")
    db.execute("SELECT title FROM content WHERE netflix_id = %s", (nid,))

    print("Content title: ", db.fetchall()[0][0])

    print("What would you like to edit?")
    print("1. Content Title     		8.  Actor 4")
    print("2. Content Type 				9.  Director")
    print("3. Content PG Rating 		10. Content category")
    print("4. Content release year		11. IMDB Rating")
    print("5. Actor 1 					12. Runtime")
    print("6. Actor 2 					13. Description")
    print("7. Actor 3 					14. Language")

    c = input("Enter your choice: ")

    if c == 1:
        title = input("Enter content title: ")

        if title:
            db.execute("UPDATE content SET title = %s WHERE netflix_id = %s", (title, nid))
            cdb.commit()
            print("Title changed successfully!")

        else:
            print("No title provided!")
        
    elif c == 2:
        type = input("Enter content type: ")

        if type:
            db.execute("UPDATE content SET type = %s WHERE netflix_id = %s", (type, nid))
            cdb.commit()
            print("Type changed successfully!")

        else:
            print("No type provided!")
            
    elif c == 3:
        rating = input("Enter content PG Rating: ")

        if rating:
            db.execute("UPDATE content SET rating = %s WHERE netflix_id = %s", (rating, nid))
            cdb.commit()
            print("Rating changed successfully!")

        else:
            print("No rating provided!")
		
    elif c == 4:
        release_year = input("Enter content release year: ")

        if release_year:
            db.execute("UPDATE content SET release_year = %s WHERE netflix_id = %s", (release_year, nid))
            cdb.commit()
            print("Release year changed successfully!")

        else:
            print("No title provided!")
            
    elif c == 5:
        actor1 = input("Enter Actor 1: ")

        if actor1:
            rc = record_checker('actors', 'id', actor1)
            db.execute("UPDATE content SET actor1 = %s WHERE netflix_id = %s",
                       (actor1, nid)) if rc == True else print("Record not added")
            cdb.commit()
            print("Actor 1 changed successfully!")

        else:
            print("No actor provided!")
            
    elif c == 6:
        actor2 = input("Enter Actor 2: ")

        if actor2:
            rc = record_checker('actors', 'id', actor2)
            db.execute("UPDATE content SET actor2 = %s WHERE netflix_id = %s",
                       (actor2, nid)) if rc == True else print("Record not added")
            cdb.commit()
            print("Actor 2 changed successfully!")

        else:
            print("No actor provided!")
            
    elif c == 7:
        actor3 = input("Enter Actor 3: ")

        if actor3:
            rc = record_checker('actors', 'id', actor3)
            db.execute("UPDATE content SET actor3 = %s WHERE netflix_id = %s",
                       (actor3, nid)) if rc == True else print("Record not added")
            cdb.commit()
            print("Actor 3 changed successfully!")

        else:
            print("No actor provided!")
            
    elif c == 8:
        actor4 = input("Enter Actor 4: ")

        if actor4:
            rc = record_checker('actors', 'id', actor4)
            db.execute("UPDATE content SET actor4 = %s WHERE netflix_id = %s",
                       (actor4, nid)) if rc == True else print("Record not added")
            cdb.commit()
            print("Actor 4 changed successfully!")

        else:
            print("No actor provided!")
            
    elif c == 9:
        director = input("Enter Director: ")

        if director:
            rc = record_checker('directors', 'id', director)
            db.execute("UPDATE content SET director = %s WHERE netflix_id = %s",
                       (director, nid)) if rc == True else print("Record not added")
            cdb.commit()
            print("Director changed successfully!")

        else:
            print("No director provided!")
            
    elif c == 10:
        category = input("Enter content Title: ")

        if category:
            db.execute("UPDATE content SET category = %s WHERE netflix_id = %s", (category, nid))
            cdb.commit()
            print("Category changed successfully!")

        else:
            print("No category provided!")
            
    elif c == 11:
        rating = input("Enter IMDB rating: ")

        if rating:
            db.execute("UPDATE content SET rating = %s WHERE netflix_id = %s", (rating, nid))
            cdb.commit()
            print("IMDB rating changed successfully!")

        else:
            print("No rating provided!")
            
    elif c == 12:
        runtime = int(input("Enter content length in minutes: "))

        if runtime:
            runtime += "min"
            db.execute("UPDATE content SET runtime = %s WHERE netflix_id = %s", (runtime, nid))
            cdb.commit()
            print("Content length changed successfully!")

        else:
            print("No length provided!")
            
    elif c == 13:
        desc = input("Enter content description: ")

        if desc:
            db.execute("UPDATE content SET desc = %s WHERE netflix_id = %s", (desc, nid))
            cdb.commit()
            print("Description changed successfully!")

        else:
            print("No description provided!")
            
    elif c == 14:
        lang = input("Enter language: ")

        if lang:
            db.execute("UPDATE content SET language = %s WHERE netflix_id = %s", (lang, nid))
            cdb.commit()
            print("Language changed successfully!")

        else:
            print("No language provided!")


def remove_actor():
    x = input("WARNING! YOU ARE ATTEMTPING TO REMOVE RECORDS FROM THE DATABASE! TYPE 'I know what I'm doing' (Case Sensitive) TO CONTINUE: ")
    if x != "I know what I'm doing":
        sys.exit("Wrong phrase entered!")

    else:
        acn = input("Enter actor ID: ")
        db.execute("SELECT name FROM actors WHERE id = %s", (acn,))
        print("Actor name: ", db.fetchall()[0][0])
        print("Would you like to delete this actor? NOTE: THIS ACTION IS IRREVERSIBLE")
        cfm = input("Type 'I Confirm' (Case Sensitive) to continue: ")

        if cfm != "I Confirm":
            sys.exit("Wrong phrase entered!")

        else:
            db.execute("DELETE FROM actors WHERE id = %s", (acn,))
            cdb.commit()
            print("Actor successfully deleted!")


def remove_director():
    x = input("WARNING! YOU ARE ATTEMTPING TO REMOVE RECORDS FROM THE DATABASE! TYPE 'I know what I'm doing' (Case Sensitive) TO CONTINUE: ")
    if x != "I know what I'm doing":
        sys.exit("Wrong phrase entered!")

    else:
        drn = input("Enter director ID: ")
        db.execute("SELECT name FROM directors WHERE id = %s", (drn,))
        print("Director name: ", db.fetchall()[0][0])
        print("Would you like to delete this director? NOTE: THIS ACTION IS IRREVERSIBLE")
        cfm = input("Type 'I Confirm' (Case Sensitive) to continue: ")

        if cfm != "I Confirm":
            sys.exit("Wrong phrase entered!")

        else:
            db.execute("DELETE FROM directord WHERE id = %s", (drn,))
            cdb.commit()
            print("Director successfully deleted!")


def remove_content():
    x = input("WARNING! YOU ARE ATTEMTPING TO REMOVE RECORDS FROM THE DATABASE! TYPE 'I know what I'm doing' (Case Sensitive) TO CONTINUE: ")
    if x != "I know what I'm doing":
        sys.exit("Wrong phrase entered!")

    else:
        cid = input("Enter content ID: ")
        db.execute("SELECT name FROM content WHERE netflix_id = %s", (cid,))
        print("Content name: ", db.fetchall()[0][0])
        print("Would you like to delete this actor? NOTE: THIS ACTION IS IRREVERSIBLE")
        cfm = input("Type 'I Confirm' (Case Sensitive) to continue: ")
        
        if cfm != "I Confirm":
            sys.exit("Wrong phrase entered!")

        else:
            db.execute("DELETE FROM content WHERE netflix_id = %s", (cid,))
            cdb.commit()
            print("Content successfully deleted!")


def login():
    global login_status
    global login_username
    login_username = input("Enter your username: ")
    password = getpass("Enter your password: ")
    db.execute("SELECT username, passhash FROM auth")
    while True:

        for i in db.fetchall():

            try:
                c = pass_verify(i[1], password)
            except argon2.exceptions.VerifyMismatchError:
                sys.exit("Incorrect password!")

            if i[0] == login_username and c == True:
                login_status = True
                os.system('cls')
                print("Login successful!")
                print("Hello,", login_username + "!" "\n")
                return login_status
                break

            elif i[0] != login_username or c == False:
                login_status = False
                sys.exit("Incorrect username!")

            else:
                login_status = False
                sys.exit("Unknown error occured!")

        break


def logout():
    global login_status
    global login_username
    print("You are now logged out!")
    login_status = False
    login_username = None


def search_content(c):
    db.execute("SELECT netflix_id, title FROM content WHERE title LIKE %s", ('%' + c + '%',))
    rs = db.fetchall()
    if len(rs) == 0:
        return "No content found!"
    else:
        return rs


def list_info(id):
    db.execute("SELECT title, release_year, rating, type, runtime, language, actor1, actor2, actor3, actor4, director, imdb, description, (price + ((price*vat)/100)) FROM content WHERE netflix_id = %s", (id,))
    rs = db.fetchall()[0]
    print()

    ac1 = actors.get(rs[6])
    ac2 = '| ' + actors.get(rs[7]) if actors.get(rs[7]) != "NULL" else ''
    ac3 = '| ' + actors.get(rs[8]) if actors.get(rs[8]) != "NULL" else ''
    ac4 = '| ' + actors.get(rs[9]) if actors.get(rs[9]) != "NULL" else ''

    if rs[7] == "NULL":
        ac2 = ac3 = ac4 = ''

    elif rs[8] == "NULL":
        ac3 = ac4 = ''

    elif rs[9] == "NULL":
        ac4 = ''

    print(termcolor.colored(rs[0].upper(), 'red', attrs=['bold', 'underline']))
    print("Release Year:", rs[1])
    print("Rating:", rs[2])
    print("Contenet Type:", rs[3])
    print("Runtime:", rs[4])
    print("Langauge:", rs[5])
    print("Starring:", ac1, ac2, ac3, ac4)
    print("Directors:", directors.get(rs[10]))
    print("IMDB Rating:", rs[11])
    print("Description:", rs[12])
    print("Price: AED", rs[13])
    print()


def luhn(ccn):
    c = [int(x) for x in str(ccn)[::-2]]
    u2 = [(2*int(y))//10+(2*int(y))%10 for y in str(ccn)[-2::-2]]
    return sum(c+u2)%10 == 0


while True:
    print("1. Login")
    print("2. Register")
    print("0. Exit")
    ch = input("Enter your choice: ")
    if ch == '1':
        login()

    elif ch == '2':
        register_customer()

    elif ch == 'admin':
        otp = gen_otp()
        send_mail("tp.cs50test@gmail.com", "tahayparker@gmail.com", "Your Netflix Admin OTP",
                  "Here's your Netflix Admin OTP<br>" + "<b>" + otp + "</b>" + "<br><b> DO NOT SHARE THIS CODE WITH ANYONE!</b>")
        input_otp = int(input("Enter OTP: "))
        if str(input_otp) == otp:
            print("Access granted")
        else:
            sys.exit("Access denied - Incorrect OTP")

        print("1. Add Functions")
        print("2. Edit Functions")
        print("3. Delete functions")
        a = int(input("Enter your choice: "))
        if a == 1:
            while True:
                print("1. Add Content")
                print("2. Add Actors")
                print("3. Add Direcors")
                print("0. Exit")
                
                b = int(input("Enter your choice: "))
                if b == 1:
                    add_content()
                
                elif b == 2:
                    add_actor()

                elif b == 3:
                    add_director

                elif b == 0:
                    break
        
        elif a == 2:
            while True:
                print("1. Edit Content")
                print("2. Edit Actors")
                print("3. Edit Direcors")
                print("0. Exit")

                c = int(input("Enter your choice: "))
                if c == 1:
                    edit_content()

                elif c == 2:
                    edit_actor()
                
                elif c == 3:
                    edit_director()

                elif c == 0:
                    break

        elif a == 3:
            while True:
                print("1. Delete Content")
                print("2. Delete Actors")
                print("3. Delete Direcors")
                print("0. Exit")

                d = int(input("Enter your choice: "))
                if d == 1:
                    remove_content()

                elif d == 2:
                    remove_actor()
                
                elif d == 3:
                    remove_director()

                elif d == 0:
                    break

    elif ch == '0':
        sys.exit("Application exited successfully!")

    else:
        sys.exit("Option not found!")

    break

while True:
    if login_status != True:
        sys.exit("Please login to continute")        
    else:
        print("1. Search for content")
        print("2. View Cart")
        print("3. Accounnt settings")
        print("0. Exit")

        sch = input("Enter your choice: ")

        if sch == '1':
            print()
            print("1. Search for content using title")
            print("2. Search for content using Netflix ID")
            print("3. List all content")
            
            ch = int(input("Enter your choice: "))
            if ch == 1:
                while True:
                    name = input("Enter content title to search: ")
                    print(name)
                    rs = search_content(name)
                    if rs == "No content found!":
                        print("No content found!")
                        print()
                        break
                    
                    for i in range(0, len(rs)):
                        print(str(i+1)+".", rs[i][1])
                    print()
                    s = int(input("Enter content number for more options:"))
                    sid = rs[s-1][0]
                    list_info(sid)

                    print("1. Buy now!")
                    print("2. Add to cart")
                    co = int(input("Enter your choice: "))
                    if co == 1:
                        print()
                        # buy_now()
                        break

                    elif co == 2:
                        db.execute("INSERT INTO cart VALUES(%s, %s, %s)", (login_username, sid, rs[s-1][1]))
                        cdb.commit()
                        print("Added to cart!")
                        print()
                        break

                    elif co == 0:
                        break

            elif ch == 2:
                while True:
                    nid = int(input("Enter Netflix ID: "))
                    db.execute("SELECT netflix_id, title FROM content WHERE netflix_id = %s", (nid,))
                    rs = db.fetchall()
                    if len(rs) == 0:
                        print("No content found!")
                        print()
                        break
                    else:
                        rs = rs[0]
                    list_info(nid)

                    print("1. Buy now!")
                    print("2. Add to cart")
                    ct = int(input("Enter your choice: "))
                    if ct == 1:
                        print()
                        # buy_now()
                    
                    elif ct == 2:
                        db.execute("INSERT INTO cart VALUES(%s, %s, %s)", (login_username, nid, rs[1]))
                        cdb.commit()
                        print("Added to cart!")
                        print()
                        break

                    elif ct == 0:
                        break
                
            elif ch == 3:
                while True:
                    db.execute("SELECT netflix_id, title FROM content ORDER BY title")
                    rs = db.fetchall()
                    print()
                    for i in range(0, len(rs)):
                        print(str(i+1)+".", rs[i][1])
                    print()

                    s = int(input("Enter content number for more options:"))
                    if s == 0:
                        print()
                        break
                    sid = rs[s-1][0]
                    list_info(sid)
                    print("1. Buy now!")
                    print("2. Add to cart")
                    cr = int(input("Enter your choice: "))
                    if cr == 1:
                        print()
                        # buy_now()
                
                    elif cr == 2:
                        db.execute("INSERT INTO cart VALUES(%s, %s, %s)", (login_username, sid, rs[s-1][1]))
                        cdb.commit()
                        print("Added to cart!")
                        print()
                        break

                    elif cr == 0:
                        break
            
            elif ch == 0:
                continue
 
        elif sch == '2':
            while True:
                print("""                                
██████   █████  ██████  ████████ 
██      ██   ██ ██   ██    ██    
██      ███████ ██████     ██    
██      ██   ██ ██   ██    ██    
██████  ██   ██ ██   ██    ██    
                """)
                db.execute("SELECT DISTINCT * FROM cart WHERE username = %s", (login_username,))
                rs = db.fetchall()
                
                if len(rs) == 0:
                    print(termcolor.colored("Your cart looks empty :(", attrs=['bold']))
                    print('\x1B[3m' + "What are you waiting for?" + '\x1B[0m')
                    print()
                    break
                    
                for i in range(0, len(rs)):
                    print(str(i+1)+".", rs[i][2])
                print()

                print("1. View movie details")
                print("2. Delete specific items")
                print("3. Empty cart")

                s = int(input("Enter your choice: "))
                
                if s == 1:
                    c = int(input("Enter content number: "))
                    sid = rs[c-1][1]
                    list_info(sid)

                    c = int(input("Press 1 to buy now: "))

                    if c == 1:
                        print()
                        # buy_now()

                elif s == 2:
                    c = int(input("Enter content number: "))
                    sid = rs[c-1][1]
                    db.execute("DELETE FROM cart WHERE username = %s AND netflix_id = %s", (login_username, sid))
                    cdb.commit()
                    print("Successfully deleted content!")
                    print()

                elif s == 3:
                    db.execute("DELETE FROM cart WHERE username = %s", (login_username,))
                    cdb.commit()
                    print("Successfully emptied cart!")
                    print()
                    break

                elif s == 0:
                    break
        
        elif sch == '0':
            sys.exit("Application exited successfully!")