import os
import datetime
import time

from modules.config import *
from modules.binance import BinanceData


class DataUpdate:
    def __init__(self, start_date, end_date, token_list, interval_list):
        self.bd = BinanceData()
        self.interval_list = interval_list
        self.token_list = token_list
        self.end_date = datetime.datetime.fromtimestamp(end_date)
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.years = self.end_date.year - self.start_date.year + 1 # +1 это константа
        self.total_kvart_number = ((self.years-1) * 12 + self.end_date.month)//3 # -1 так как последний год не полный, 12 это количество месяцев, 3 это размер квартала
        self.kvartals = ({'start':{'month':1,'day':1}, 'end':{'month':3,'day':31}}, 
                    {'start':{'month':4,'day':1}, 'end':{'month':6,'day':30}},
                    {'start':{'month':7,'day':1}, 'end':{'month':9,'day':30}},
                    {'start':{'month':10,'day':1}, 'end':{'month':12,'day':31}})

    def get_periods(self):
        year = self.start_date.year
        i = 0
        periods = []
        for _ in range(self.total_kvart_number):
            _start_date, _end_date = self.get_kvart_data(year, i)
            periods.append((year, i+1, _start_date, _end_date))
            i+=1
            if i > 3:
                i = 0
                year+=1
        _start_date, _ = self.get_kvart_data(year, i)
        periods.append((year, i+1, _start_date, self.end_date))
        return periods

    def create_dir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def get_kvart_data(self, year, i):
        start_month, end_month = self.kvartals[i]['start']['month'], self.kvartals[i]['end']['month']
        start_day, end_day = self.kvartals[i]['start']['day'], self.kvartals[i]['end']['day']
        _start_date = datetime.datetime(year, start_month, start_day)
        _end_date = datetime.datetime(year, end_month, end_day, 23, 59, 59) # Тут 23:59:59 Означает конец дня
        return _start_date, _end_date

    def get_data(self, token, year, i, start_date, end_date):
        for interval in self.interval_list:
            if not os.path.exists(f'data/{token}USDT/{year}_{i}/{interval}.csv'):
                df = self.bd.get_historical_candles(symbol=token, start_date=start_date, end_date=end_date, interval=interval)
                df.to_csv(f'data/{token}USDT/{year}_{i}/{interval}.csv', index=False)

    def core(self, token):
        for period in self.get_periods():
            year = period[0]
            i = period[1]
            start_date = period[2]
            end_date = period[3]
            self.create_dir(f'data/{token}USDT/{year}_{i+1}')
            self.get_data(token, year, i, start_date, end_date)

    def run(self):
        self.create_dir('data')
        for token in self.token_list:
            print(token)
            self.create_dir(f'data/{token}USDT')
            self.core(token)