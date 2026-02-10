import sqlite3


conn = sqlite3.connect("app.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password_hash TEXT NOT NULL,
               created_at TEXT NOT NULL
)
""")


cursor2 = conn.cursor()

cursor2.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                result TEXT NOT NULL,
                timestamp TEXT NOT NULL
)
""")

conn.commit()

