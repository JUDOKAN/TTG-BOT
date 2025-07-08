import os
import sqlite3
import boxing2d_logic
import driverush2d_logic
import rocketdrift2d_logic
import snakegame2d_logic
import mathdash_logic
from config import DB_FOLDER, DB_PATH_GENERAL

def init_all_dbs():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    boxing2d_logic.init_db()
    driverush2d_logic.init_db()
    rocketdrift2d_logic.init_db()
    snakegame2d_logic.init_db()
    mathdash_logic.init_db()

    conn = sqlite3.connect(DB_PATH_GENERAL)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS general_scores (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_name TEXT UNIQUE NOT NULL,
               boxing2d_score INTEGER DEFAULT 0,
               driverush2d_score INTEGER DEFAULT 0,
               rocketdrift2d_score INTEGER DEFAULT 0,
               snakegame2d_score INTEGER DEFAULT 0,
               mathdash_score INTEGER DEFAULT 0
           )'''
    )
    conn.commit()
    conn.close()

def register_user(user_name: str):
    conn = sqlite3.connect(DB_PATH_GENERAL)
    c = conn.cursor()
    c.execute(
        'INSERT OR IGNORE INTO general_scores (user_name) VALUES (?)',
        (user_name,)
    )
    conn.commit()
    conn.close()

def update_general_score(user_name: str, game_key: str, score: int):
    field = f'{game_key}_score'
    conn = sqlite3.connect(DB_PATH_GENERAL)
    c = conn.cursor()
    c.execute(
        f'UPDATE general_scores SET {field} = {field} + ? WHERE user_name = ?',
        (score, user_name)
    )
    conn.commit()
    conn.close()

def get_top_general(limit: int = 10):
    conn = sqlite3.connect(DB_PATH_GENERAL)
    c = conn.cursor()
    c.execute(
        '''SELECT user_name,
                  (boxing2d_score + driverush2d_score + rocketdrift2d_score +
                   snakegame2d_score + mathdash_score) as total
           FROM general_scores
           ORDER BY total DESC
           LIMIT ?''',
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def get_general_rank(user_name: str):
    conn = sqlite3.connect(DB_PATH_GENERAL)
    c = conn.cursor()
    c.execute(
        '''SELECT COUNT(*)+1 FROM (
               SELECT user_name,
                      (boxing2d_score + driverush2d_score + rocketdrift2d_score +
                       snakegame2d_score + mathdash_score) as total
               FROM general_scores
               ORDER BY total DESC
           ) WHERE total >
               (SELECT (boxing2d_score + driverush2d_score + rocketdrift2d_score +
                        snakegame2d_score + mathdash_score)
                FROM general_scores WHERE user_name = ?)''',
        (user_name,)
    )
    rank = c.fetchone()[0]
    conn.close()
    return rank