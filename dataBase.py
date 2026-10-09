import sqlite3

class dataBase:
    def __init__(self):
        self.dbname = 'database.db'
        self.conn = sqlite3.connect(self.dbname)
        self.setUp()

    def setUp(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')

        count = cursor.execute('SELECT COUNT(*) FROM category').fetchone()[0]
        if count == 0:
            cursor.executemany(
                'INSERT INTO category (name, type) VALUES (?,?)',
                [
                    ("食費","支出",),
                    ("生活費","支出",),
                    ("住居費","支出",),
                    ("医療費","支出",)
                ]
            )

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount REAL,
                category_id INTEGER,
                bank TEXT,
                balance TEXT,
                FOREIGN KEY (category_id) REFERENCES category(id)
            )
        ''')

        self.conn.commit()

    def exeQuery(self, query, values):
        cursor = self.conn.cursor()
        cursor.execute(query,values)
        self.conn.commit()
        return cursor
    
    def fetchQuery(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        #items = cursor.fetchall()
        return cursor

    def close(self):
        self.conn.close()
