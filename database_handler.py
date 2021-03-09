import sqlite3 
from flask import g

DATABASE_URI = 'database.db'

# connect to the database
def get_db():
    db = getattr(g, 'db', None)
    if db is None:
         db = g.db = sqlite3.connect(DATABASE_URI)
    return db

# disconnect from the database
def disconnect_db():
    db = getattr(g, 'db, None')
    if db is None:
        g.db.close()
        g.db = None

# try to save a new user in the databse, if error -> return false
def save_user(email, password, first_name, family_name, gender, country, city):
    try: 
        get_db().execute("insert into users values(?,?,?,?,?,?,?);", [email, password, first_name, family_name, gender, country, city])
        get_db().commit()
    except:
        return False
    return True

# update a user password, if error -> return false
def update_password(email, password):
    try:
        get_db().execute("update users set password = ? where email = ?;", [password, email])
        get_db().commit()
        return True
    except: 
        return False

# retrieve user information from email 
def get_user(email):
    cursor = get_db().execute("select * from users where email like ?", [email])
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for index in range(len(rows)):
        result.append({'email': rows[index][0], 'password': rows[index][1], 'first_name': rows[index][2],  'family_name': rows[index][3],  'gender': rows[index][4],  'country': rows[index][5],  'city': rows[index][6]})
    return result

# get all user messaged based on the email
def get_user_messages_by_email(email):
    cursor = get_db().execute("select * from messages where email like ?", [email])
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for index in range(len(rows)):
        result.append({'email': rows[index][0], 'writer': rows[index][1], 'message': rows[index][2]})
    return result

# post a message to a persons wall with a defined author/writer
def post_message(email, writer, message):
    try: 
        get_db().execute("insert into messages values(?,?,?);", [email, writer, message])
        get_db().commit()
    except:
        return False
    return True

