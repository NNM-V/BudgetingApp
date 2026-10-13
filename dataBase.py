import sqlite3

class dataBase:
    def __init__(self):
        self.dbname = 'database.db'
        self.conn = sqlite3.connect(self.dbname)
        self.setUp()

    def setUp(self):
        cursor = self.conn.cursor()
        # Create category table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        # Insert initial data once when table is created
        categoryCount = cursor.execute('SELECT COUNT(*) FROM category').fetchone()[0]
        if categoryCount == 0:
            cursor.executemany(
                'INSERT INTO category (name, type) VALUES (?,?)',
                [
                    ("食費","支出",),
                    ("生活費","支出",),
                    ("住居費","支出",),
                    ("医療費","支出",),
                    ("給料","収入",),
                    ("お小遣い","収入")
                ]
            )
        # Create bank table if not exists    
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bank (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        # Insert initial data once when table is created
        bankCount = cursor.execute('SELECT COUNT(*) FROM bank').fetchone()[0]
        if bankCount == 0:
            cursor.executemany(
                'INSERT INTO bank (name) VALUES (?)',
                [
                    ("銀行",),
                    ("財布",)
                ]
            )
        #Create report table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount REAL,
                category_id INTEGER,
                bank_id  INTEGER,
                balance TEXT,
                FOREIGN KEY (category_id) REFERENCES category(id)
                FOREIGN KEY (bank_id) REFERENCES bank(id)
            )
        ''')
        # Save transaction to database
        self.conn.commit()

    def exeQuery(self, query, values):
        cursor = self.conn.cursor()
        # Execute query
        cursor.execute(query,values)
        # Save transaction to database
        self.conn.commit()
        return cursor
    
    def fetchQuery(self, query):
        cursor = self.conn.cursor()
        # Execute query
        cursor.execute(query)
        return cursor

    def close(self):
        self.conn.close()
