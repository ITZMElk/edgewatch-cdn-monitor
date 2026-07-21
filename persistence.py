"""SQLite persistence for telemetry, activity events, and local users."""
import json
import sqlite3
from pathlib import Path
from threading import Lock

DB_PATH = Path(__file__).with_name("edgewatch.db")
_lock = Lock()


def _connection():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with _lock, _connection() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS requests (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          payload TEXT NOT NULL,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS activity (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          timestamp TEXT NOT NULL,
          message TEXT NOT NULL,
          level TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS users (
          username TEXT PRIMARY KEY,
          password_hash TEXT NOT NULL,
          role TEXT NOT NULL);
        """)


def initialize():
    init_db()


def save_request(record):
    init_db()
    with _lock, _connection() as con:
        con.execute("INSERT INTO requests(payload) VALUES (?)", (json.dumps(record),))
        con.execute("DELETE FROM requests WHERE id NOT IN (SELECT id FROM requests ORDER BY id DESC LIMIT 100)")


def load_requests():
    try:
        init_db()
        with _lock, _connection() as con:
            rows = con.execute("SELECT payload FROM requests ORDER BY id DESC LIMIT 100").fetchall()
    except (sqlite3.OperationalError, sqlite3.DatabaseError):
        return []
    return [json.loads(row["payload"]) for row in rows]


def log_activity(timestamp, message, level="info"):
    with _lock, _connection() as con:
        con.execute("INSERT INTO activity(timestamp,message,level) VALUES (?,?,?)", (timestamp, message, level))
        con.execute("DELETE FROM activity WHERE id NOT IN (SELECT id FROM activity ORDER BY id DESC LIMIT 200)")


def get_activity():
    with _lock, _connection() as con:
        return [dict(row) for row in con.execute("SELECT timestamp,message,level FROM activity ORDER BY id DESC LIMIT 100")]


def ensure_user(username, password_hash, role="admin"):
    with _lock, _connection() as con:
        con.execute("INSERT OR IGNORE INTO users(username,password_hash,role) VALUES (?,?,?)", (username, password_hash, role))


def get_user(username):
    with _lock, _connection() as con:
        row = con.execute("SELECT username,password_hash,role FROM users WHERE username=?", (username,)).fetchone()
    return dict(row) if row else None
