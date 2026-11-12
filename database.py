import sqlite3


class DataBase:
    def __init__(self):
        self.db_name = 'database.db'
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.setup()

    def setup(self):
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
        category_count = cursor.execute(
            'SELECT COUNT(*) FROM category'
        ).fetchone()[0]
        if category_count == 0:
            cursor.executemany(
                'INSERT INTO category (name, type) VALUES (?,?)',
                [
                    ("食費", "支出",),
                    ("生活費", "支出",),
                    ("住居費", "支出",),
                    ("医療費", "支出",),
                    ("給料", "収入",),
                    ("お小遣い", "収入")
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
        bank_count = cursor.execute('SELECT COUNT(*) FROM bank').fetchone()[0]
        if bank_count == 0:
            cursor.executemany(
                'INSERT INTO bank (name) VALUES (?)',
                [
                    ("銀行",),
                    ("財布",)
                ]
            )
        # Create budget table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budget (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year_month TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                amount REAL,
                UNIQUE(year_month, category_id),
                FOREIGN KEY (category_id) REFERENCES category(id)
            )
        ''')
        # Create report table if not exists
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

    def exe_query(self, query, values=None):
        # Automatically close database when done
        with self.conn:
            cursor = self.conn.cursor()
            # Execute query
            try:
                if values is not None:
                    cursor.execute(query, values)
                    self.conn.commit()
                else:
                    cursor.execute(query)
                    self.conn.commit()
            except sqlite3.Error as e:
                print(f"An error occured: {e}")
                self.conn.rollback()

        return cursor

    def fetch_query(self, query, values=None, balance=None):
        # Automatically close database when done
        with self.conn:
            cursor = self.conn.cursor()
            # Execute query
            try:
                if values is not None:
                    cursor.execute(query, values)
                elif balance is not None:
                    cursor.execute(query, values, balance)
                else:
                    cursor.execute(query)
            except sqlite3.Error as e:
                print(f"An error occured: {e}")
                self.conn.rollback()

        return cursor

    def close(self):
        self.conn.close()
