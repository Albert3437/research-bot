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
    def __init__(self, db_name:str, period_strings):
        super().__init__()
        self.db_name = db_name 
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS {name} (
                id INTEGER PRIMARY KEY,
                arch TEXT,
                arch_type TEXT,
                interval TEXT,
                comb_number INTEGER,
                comb TEXT{text}
                )
            '''.format(name = self.db_name, text = period_strings))


    @logger.catch
    def write_strat(self, arch = 0, arch_type = 0, interval = 0, comb_number = 0, comb = 0):
        check_query = f'SELECT COUNT(*) FROM {self.db_name} WHERE arch=? AND arch_type=? AND interval=? AND comb_number=? AND comb=?'
        count = self.conn.execute(check_query, (arch, arch_type, interval, comb_number, comb)).fetchone()[0]
        if count == 0:
            self.conn.execute(f'INSERT INTO {self.db_name} (arch, arch_type, interval, comb_number, comb) VALUES (?,?,?,?,?)',(arch, arch_type, interval, comb_number, comb))
            self.conn.commit()


    @logger.catch
    def write_data(self, year, period, totalProfit, dealsNumber, profitPercent, avgPercent, minPercent, maxPercent, arch = 0, arch_type = 0, interval = 0, comb_number = 0, comb = 0):
        # Подготавливаем SQL-запрос для обновления строки
        update_query = f'UPDATE {self.db_name} SET '
        
        # Формируем список аргументов и их значений для обновления
        update_query += f'totalProfit{year}_{period}=?, dealsNumber{year}_{period}=?, profitPercent{year}_{period}=?, avgPercent{year}_{period}=?, minPercent{year}_{period}=?, maxPercent{year}_{period}=?'
        update_args = [totalProfit, dealsNumber, profitPercent, avgPercent, minPercent, maxPercent]
        
        # Удаляем последнюю запятую и добавляем условие для выбора строки для обновления
        update_query += f' WHERE arch=? AND arch_type=? AND interval=? AND comb_number=? AND comb=?'
        
        # Добавляем аргументы для условия WHERE
        update_args.extend([arch, arch_type, interval, comb_number, comb])
        
        # Выполняем запрос на обновление
        self.conn.execute(update_query, update_args)
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