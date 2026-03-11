import sqlite3


def create_tables():
    conn = sqlite3.connect("farmmind.db")
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Chat history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question TEXT,
            answer TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_chat(user_id, question, answer):
    conn = sqlite3.connect("farmmind.db")
    c = conn.cursor()

    c.execute("INSERT INTO chats (user_id, question, answer) VALUES (?, ?, ?)",
              (user_id, question, answer))

    conn.commit()
    conn.close()
