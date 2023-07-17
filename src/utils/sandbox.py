import sqlite3

class Song:

    def __init__(self, name, album):
        self.name = name
        self.album = album
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """

        CURSOR.execute(sql)

import ipdb; ipdb.set_trace()

CONN = sqlite3.connect('music.db')
CURSOR = CONN.cursor()

Song.create_table()

CURSOR.execute("PRAGMA table_info(songs)").fetchall()
# => [(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0), (2, 'album', 'TEXT', 0, None, 0)]