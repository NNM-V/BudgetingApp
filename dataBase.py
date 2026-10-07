import sqlite3

class dataBase:
    def __init__(self):
        self.dbname = 'database.db'
        self.conn = sqlite3.connect(self.dbname)
        self.setUp()

    def setUp(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount REAL,
                category TEXT,
                bank TEXT,
                balance Text
            )
        """)

        self.conn.commit()

    def exeQuery(self, query, values):
        cursor = self.conn.cursor()
        cursor.execute(query,values)
        self.conn.commit()

    def close(self):
        self.conn.close()
