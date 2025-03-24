import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    #drop table
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            location TEXT,
            temp INTEGER,
            humd INTEGER,
            sky TEXT,
            rain INTEGER,
            otp INTEGER,
            language TEXT,
            password TEXT
        )
    """)
    #create table to store fertilizer details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fertilizer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            name TEXT
        )
    """)
    conn.commit()
    conn.close()

# Register a new user
def register_user(name, email,location, temp, humd, sky, rain,otp,language, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, location, temp, humd, sky, rain, otp,language, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)", (name, email, location, temp, humd, sky, rain, otp,language, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# Validate login credentials
def validate_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def valid_user(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def change_location(email,location,temp,humd,sky,rain,language):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET location = ?, temp = ?, humd = ?, sky = ?, rain = ?, language = ? WHERE email = ?", (location,temp,humd,sky,rain,language,email))
    conn.commit()
    conn.close()

def fetch_details(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_otp(email,otp):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET otp = ? WHERE email = ?", (otp, email))
    conn.commit()
    conn.close()

def fetch_otp(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT otp FROM users WHERE email = ?", (email,))
    otp = cursor.fetchone()
    conn.close()
    return otp

def update_password(email,password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (password, email))
    conn.commit()
    conn.close()

def fetch_password(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    password = cursor.fetchone()
    conn.close()
    return password

def add_fertilizer(email,name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fertilizer (email, name) VALUES (?, ?)", (email, name))
    conn.commit()
    conn.close()
def fetch_fertilizer(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM fertilizer WHERE email = ?", (email,))
    fertilizer = cursor.fetchall()
    conn.close()
    return fertilizer