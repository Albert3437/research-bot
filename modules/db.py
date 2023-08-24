import sqlite3
from modules.logger import logger

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')


    @logger.catch
    def read_db(self, db_name):
        cursor = self.conn.execute(f"SELECT * FROM {db_name}")
        return cursor.fetchall()
    

    @logger.catch
    def read_header(self, db_name):
        data = self.conn.execute(f'PRAGMA table_info({db_name})')
        column_headers = [row[1] for row in data.fetchall()]
        return column_headers


    @logger.catch
    def read_dict_db(self, db_name):
        head = self.read_header(db_name)
        deals = self.read_db(db_name)
        dict_deals = []
        for deal in deals:
            dict_deal = {}
            for i, amount in enumerate(deal):
                dict_deal[head[i]] = amount
            dict_deals.append(dict_deal)
        return dict_deals


    @logger.catch
    def remove_table(self, db_name):
        self.conn.execute(f'DROP TABLE {db_name}')


    @logger.catch
    def clear_db(self, db_name):
        self.conn.execute(f"DELETE FROM {db_name}")
        self.conn.commit()


    @logger.catch
    def close_db(self):
        self.conn.close()



class StratsDataBase(DataBase):
    def __init__(self, db_name:str):
        super().__init__()
        self.db_name = db_name 
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS {} (
                id INTEGER PRIMARY KEY,
                arch TEXT,
                arch_type TEXT,
                year INTEGER,
                interval TEXT,
                comb_number INTEGER,
                comb TEXT,
                totalProfit REAL,
                dealsNumber REAL,
                profitPercent REAL,
                avgPercent REAL,
                minPercent REAL,
                maxPercent REAL
                )
            '''.format(self.db_name))


    @logger.catch
    def write_strat(self, arch = 0, arch_type = 0, year = 0, interval = 0, comb_number = 0, comb = 0, totalProfit = 0, dealsNumber = 0, profitPercent = 0, avgPercent = 0, minPercent = 0, maxPercent = 0):
        self.conn.execute(f'INSERT INTO {self.db_name} (arch, arch_type, year, interval, comb_number, comb, totalProfit, dealsNumber, profitPercent, avgPercent, minPercent, maxPercent) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(arch, arch_type, year, interval, comb_number, comb, totalProfit, dealsNumber, profitPercent, avgPercent, minPercent, maxPercent))
        self.conn.commit()


    @logger.catch
    def read_strats(self, db_name = None):
        if db_name == None:
            db_name = self.db_name
        deals = self.read_dict_db(db_name)
        return deals
    

    @logger.catch
    def clear_strats(self):
        self.clear_db(self.db_name)