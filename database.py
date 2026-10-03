import sqlite3
import config

def get_connection():
    conn = sqlite3.connect(config.DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0,
            correct_captcha INTEGER DEFAULT 0,
            wrong_captcha INTEGER DEFAULT 0,
            referred_by INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS withdrawals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            method TEXT,
            account_details TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, username, referred_by=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if not cursor.fetchone():
        cursor.execute('INSERT INTO users (user_id, username, referred_by) VALUES (?, ?, ?)',
                       (user_id, username, referred_by))
        if referred_by:
            cursor.execute('UPDATE users SET balance = balance + 30.0 WHERE user_id = ?', (referred_by,))
        conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_captcha_stat(user_id, is_correct, reward=3.0):
    conn = get_connection()
    cursor = conn.cursor()
    if is_correct:
        cursor.execute('UPDATE users SET balance = balance + ?, correct_captcha = correct_captcha + 1 WHERE user_id = ?', (reward, user_id))
    else:
        cursor.execute('UPDATE users SET wrong_captcha = wrong_captcha + 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
