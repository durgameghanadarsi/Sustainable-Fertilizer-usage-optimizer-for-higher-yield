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
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS otp_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            otp INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Register a new user
def register_user(name, email,location, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email,location, password) VALUES (?, ?, ?,?)", (name, email,location, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
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

# Store OTP for a user
def store_otp(email, otp):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO otp_data (email, otp) VALUES (?, ?)", (email, otp))
    conn.commit()
    conn.close()

# Validate OTP
def validate_otp(email, otp):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM otp_data WHERE email = ? AND otp = ?", (email, otp))
    valid = cursor.fetchone()
    conn.close()
    return valid

# Update user password
def update_password(email, new_password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
    conn.commit()
    conn.close()
