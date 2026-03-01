import sqlite3
import datetime

class TradeJournal:
    def __init__(self, db_name="journal.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                symbol TEXT,
                side TEXT,
                amount REAL,
                price REAL,
                strategy_reason TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def log_trade(self, symbol, side, amount, price, reason, status="executed"):
        ts = datetime.datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO trades (timestamp, symbol, side, amount, price, strategy_reason, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (ts, symbol, side, amount, price, reason, status))
        self.conn.commit()
