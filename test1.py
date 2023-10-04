import time
from modules.collect_data import DataUpdate
from modules.config import *
from modules.db import StratsDataBase


du = DataUpdate(START_DATE, END_DATE, TOKEN_LIST, INTERVALS)


text = ''
for period in du.get_periods():
    example = ',totalProfit{year}_{period} REAL,dealsNumber{year}_{period} REAL,profitPercent{year}_{period} REAL,avgPercent{year}_{period} REAL,minPercent{year}_{period} REAL,maxPercent{year}_{period} REAL'.format(year=period[0], period=period[1])
    text += example


db = StratsDataBase('test', text)

db.write_strat()
db.write_data(2023, 3, 0, 0, 0, 0, 0, 0)

print(db.read_db('test'))