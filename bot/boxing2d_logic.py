
import sqlite3
from config import DB_PATH_BOXING2D

def init_db():
    conn = sqlite3.connect(DB_PATH_BOXING2D)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS boxing2d_scores (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_name TEXT NOT NULL,
               score INTEGER NOT NULL
           )'''
    )
    conn.commit()
    conn.close()

def add_score(user_name: str, score: int):
    conn = sqlite3.connect(DB_PATH_BOXING2D)
    c = conn.cursor()
    c.execute(
        'INSERT INTO boxing2d_scores (user_name, score) VALUES (?, ?)',
        (user_name, score)
    )
    conn.commit()
    conn.close()

def get_top_scores(limit: int = 10):
    conn = sqlite3.connect(DB_PATH_BOXING2D)
    c = conn.cursor()
    c.execute(
        'SELECT user_name, score FROM boxing2d_scores ORDER BY score DESC LIMIT ?',
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def get_user_rank(user_name: str):
    conn = sqlite3.connect(DB_PATH_BOXING2D)
    c = conn.cursor()
    c.execute(
        'SELECT COUNT(*)+1 FROM boxing2d_scores WHERE score > '
        '(SELECT score FROM boxing2d_scores WHERE user_name = ? ORDER BY id DESC LIMIT 1)',
        (user_name,)
    )
    rank = c.fetchone()[0]
    conn.close()
    return rank

