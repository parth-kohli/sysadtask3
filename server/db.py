import mysql.connector
from datetime import datetime
db_config = {
    "host": "db",
    "user": "root",
    "password": "rootpass",
    "database": "chatdb"
}
def get_db_connection():
    return mysql.connector.connect(**db_config)
def create_user(username, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    conn.commit()
    conn.close()

def verify_user(username, password_hash):
    print("1")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, password_hash))
    result = cursor.fetchone()
    conn.close()
    return result is not None
def log_message(username, room, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, room, content) VALUES (%s, %s, %s)", (username, room, content))
    conn.commit()
    conn.close()
def start_session(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (username, login_time) VALUES (%s, %s)", (username, datetime.now()))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def end_session(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET logout_time = %s WHERE id = %s", (datetime.now(), session_id))
    conn.commit()
    conn.close()
def get_room_history(room, limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, content, timestamp FROM messages WHERE room=%s ORDER BY timestamp DESC LIMIT %s",
        (room, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    return list(reversed(rows))  # Show oldest first

def get_leaderboard(limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, COUNT(*) AS msg_count FROM messages GROUP BY sender ORDER BY msg_count DESC LIMIT %s",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
def create_room(room_name):
    print(f"[DB] Creating room: {room_name}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO rooms (name) VALUES (%s)", (room_name,))
    conn.commit()
    conn.close()

def get_all_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM rooms")
    rooms = [row[0] for row in cursor.fetchall()]
    conn.close()
    return rooms

