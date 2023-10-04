import pandas as pd
from modules.config import *
from calculate import Calculation
from modules.db import StratsDataBase
from modules.logger import logger
from modules.telegram import Telegram
from modules.prepare_data import get_combinations
from modules.collect_data import DataUpdate
from modules.indicators import TechnicalIndicators
import json
import sys

du = DataUpdate(START_DATE, END_DATE, TOKEN_LIST, INTERVALS)

@logger.catch
def json_dump(data, filename):
    with open(f'{filename}.json', 'w') as f:
        json.dump(data, f)


def calc_all_indicators(df):
    ta = TechnicalIndicators(df)

    for values in INDICATOR_DICT(ta).values():
        values()

    return df


def db_columns():
    text = ''
    for period in du.get_periods():
        example = ',totalProfit{year}_{period} REAL,dealsNumber{year}_{period} REAL,profitPercent{year}_{period} REAL,avgPercent{year}_{period} REAL,minPercent{year}_{period} REAL,maxPercent{year}_{period} REAL'.format(year=period[0], period=period[1])
        text += example
    return text


@logger.catch
def run(token):
    telega = Telegram()
    strat_db = StratsDataBase(token, db_columns())
    strat_db.clear_strats()
    telega.send_message(token)
    for arch in ARCH_LIST:
        for arch_type in ARCH_TYPE:
            for period in du.get_periods():
                telega.send_message(str(period))
                for interval in INTERVALS:
                    telega.send_message(interval)
                    df = pd.read_csv(f'data/{token}USDT/{period[0]}_{period[1]}/{interval}.csv')
                    df = calc_all_indicators(df)
                    for comb_number in COMB_NUMBER_LIST:
                        for comb in get_combinations(comb_number):
                            calc = Calculation(df, arch, arch_type, comb)
                            data = calc.run()
                            strat_db.write_strat(arch, arch_type, interval, comb_number, str(comb)) # , data['totalProfit'], data['dealsNumber'], data['profitPercent'], data['avgPercent'], data['minPercent'], data['maxPercent']
                            strat_db.write_data(period[0], period[1], data['totalProfit'], data['dealsNumber'], data['profitPercent'], data['avgPercent'], data['minPercent'], data['maxPercent'], arch, arch_type, interval, comb_number, str(comb))

if __name__ == '__main__':
    index = int(sys.argv[1])
    run(TOKEN_LIST[index])
    run(TOKEN_LIST[index+5])