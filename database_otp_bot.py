# File: database_otp_bot.py

import sqlite3
import logging

DB_FILE = "otp_bot_users.db" # Nama database yang berbeda
logger = logging.getLogger(__name__)

def initialize_database():
    """Membuat database dan tabel pengguna untuk Bot OTP."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            is_authorized BOOLEAN DEFAULT 0
        )
    """)
    con.commit()
    con.close()
    logger.info(f"Database '{DB_FILE}' berhasil diinisialisasi.")

def set_user_access(user_id: int, status: bool, username: str = None, first_name: str = None):
    """Memberi atau mencabut akses, juga menambahkan user jika belum ada."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    try:
        # Tambahkan user jika belum ada
        cur.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        # Atur status otorisasi
        cur.execute(
            "UPDATE users SET is_authorized = ? WHERE user_id = ?",
            (1 if status else 0, user_id)
        )
        con.commit()
    finally:
        con.close()

def is_user_authorized(user_id: int) -> bool:
    """Mengecek apakah pengguna diizinkan akses."""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    try:
        cur.execute("SELECT is_authorized FROM users WHERE user_id = ?", (user_id,))
        result = cur.fetchone()
        return bool(result and result[0] == 1)
    finally:
        con.close()