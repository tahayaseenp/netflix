from msilib import _directories
import os
import sys
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
except:
    sys.exit("Unable to install required dependencies!")
try:
    import argon2
    import ipinfo
    import datetime
    import time
    import termcolor
    from getpass import getpass
    from mysql.connector import connect
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
db.execute("CREATE TABLE IF NOT EXISTS customers(id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL, name LONGTEXT NOT NULL, email LONGTEXT NOT NULL, phone_number LONGTEXT NOT NULL, username VARCHAR(512) NOT NULL, country_Code CHAR(3) NOT NULL, balance FLOAT NOT NULL DEFAULT 0.0)")
db.execute("CREATE TABLE IF NOT EXISTS auth(username LONGTEXT NOT NULL, passhash LONGTEXT NOT NULL, PRIMARY KEY index_username(username(100)))")
db.execute("CREATE TABLE IF NOT EXISTS orders(id BIGINT AUTO_INCREMENT PRIMARY KEY NOT NULL, customer_ID BIGINT NOT NULL, date DATETIME)")
db.execute("CREATE TABLE IF NOT EXISTS order_details(order_iD BIGINT NOT NULL, content_id BIGINT NOT NULL, amount BIGINT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS cart(netflix_id BIGINT NOT NULL, title LONGTEXT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS sudo_logs(query LONGTEXT, query_timestamp LONGTEXT)")

login_status = False


actors={}
db.execute("SELECT * FROM actors")
for i in db.fetchall():
    actors[i][0] = i[1]
print(actors)
directors = {}
db.execute("SELECT * FROM directors")
for i in db.fetchall():
    directors[i][0] = i[1]
print(directors)

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
    db.execute("INSERT INTO actors VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (netflix_id, title, type, rating, release_year, actor1, actor2, actor3, actor4,
               director, category, imdb, runtime, description, language)) if rc1 == True and rc2 == True and rc3 == True and rc4 == True and rc5 == True else print("Record not added!")
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
    print("You have successfully registered! Please run the program and login")
    sys.exit(0)


def edit_actor():
    acn = input("Enter actor ID: ")
    db.execute("SELECT name FROM actors WHERE id = %s", (acn,))
    print("Actor name: ", db.fetchall()[0])
    new = input("Enter new actor name: ")
    db.execute("UPDATE actors SET name = %s WHERE id = %s", (new, acn)) if acn else print("Actor editing failed!")
    cdb.commit()
    print("Actor successfully edited")


def edit_director():
    drn = input("Enter director ID: ")
    db.execute("SELECT name FROM directors WHERE id = %s", (drn,))
    print("Director name: ", db.fetchall()[0])
    new = input("Enter new director name: ")
    db.execute("UPDATE directors SET name = %s WHERE id = %s", (new, drn)) if drn else print("Director editing failed!")
    cdb.commit()
    print("Director successfully edited")


def edit_content():
    nid = input("Enter Netflix ID: ")
    db.execute("SELECT title FROM content WHERE netflix_id = %s", (nid,))
    print("Content title: ", db.fetchall()[0])
    type = input("Enter content type (Movie OR TV Show): ")
    print("What would you like to edit?")
    print("1. Content Title     		8. Actor 4")
    print("2. Content Type 				9. Director")
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
            print("content length changed successfully!")
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
        cdb.commit()
        print("Director successfully edited")


def remove_actor():
    x = input("WARNING! YOU ARE ATTEMTPING TO REMOVE RECORDS FROM THE DATABASE! TYPE 'I know what I'm doing' (Case Sensitive) TO CONTINUE: ")
    if x != "I know what I'm doing":
        sys.exit("Wrong phrase entered!")
    else:
        acn = input("Enter actor ID: ")
        db.execute("SELECT name FROM actors WHERE id = %s", (acn,))
        print("Actor name: ", db.fetchall()[0])
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
        print("Director name: ", db.fetchall()[0])
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
        print("Content name: ", db.fetchall()[0])
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
            c = pass_verify(i[1], password)
            if c == argon2.exceptions.VerifyMismatchError:
                sys.exit("Incorrect password!")

            if i[0] == login_username  and c == True:
                login_status = True
                os.system('cls')
                print("Login successful!")
                print("Hello,", login_username + "!" "\n")
                return login_status
                break

            elif i[0] != login_username or c == False:
                login_status = False
                sys.exit("Login failed!")
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
    return db.fetchall()


def list_info(id):
    db.execute("SELECT title, release_year, rating, type, runtime, language, actor1, actor2, actor3, actor4, director, imdb, description, (price + ((price*vat)/100)) 'price' FROM content WHERE netflix_id = %s", (id,))
    rs = db.fetchall()
    print()
    print(termcolor.colored(rs[0][0].upper(), 'red', attrs=['bold', 'underline']))
    print("Release Year: ", rs[0][1])
    print("Rating: ", rs[0][2])
    print("Contenet Type: ", rs[0][3])
    print("Runtime: ", rs[0][4])
    print("Langauge: ", rs[0][5])
    print("Actor1: ", actors.get(rs[0][6]))
    print()

while True:
    print("1. Login")
    print("2. Register")
    print("0. Exit")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        login()
    elif ch == 2:
        register_customer()
    elif ch == 0:
        sys.exit("Application exited successfully!")
    else:
        sys.exit("Option not found!")
    break

while True:
    if login_status != True:
        sys.exit("Please login to continute")        
    else:
        print("1. Search for content using title")
        print("2. Search for content using Netflix ID")
        print("3. List all content")
        print("4. Settings")
        ch = int(input("Enter your choice: "))
        if ch == 1:
            name = input("Enter content title to search: ")
            rs = search_content(name)
            for i in range(0, len(rs)):
                print(str(i+1)+".", rs[i][1])
            print()
            s = int(input("Enter content number for more options:"))
            sid = rs[s-1][0]
            list_info(sid)