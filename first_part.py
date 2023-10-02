import pandas as pd
from modules.config import *
from calculate import Calculation
from modules.db import StratsDataBase
from modules.logger import logger
from modules.telegram import Telegram
from modules.prepare_data import get_combinations
from modules.indicators import TechnicalIndicators
import json
import threading
import sys

@logger.catch
def json_dump(data, filename):
    with open(f'{filename}.json', 'w') as f:
        json.dump(data, f)


def calc_all_indicators(df):
    ta = TechnicalIndicators(df)

    for values in INDICATOR_DICT(ta).values():
        values()

    return df


@logger.catch
def run(token):
    telega = Telegram()
    strat_db = StratsDataBase(token)
    strat_db.clear_strats()
    telega.send_message(token)
    for arch in ARCH_LIST:
        for arch_type in ARCH_TYPE:
            for year in YEARS:
                telega.send_message(year)
                for interval in INTERVALS:
                    telega.send_message(interval)
                    df = pd.read_csv(f'data/{token}USDT/data_{year}/{interval}.csv')
                    df = calc_all_indicators(df)
                    for comb_number in COMB_NUMBER_LIST:
                        for comb in get_combinations(comb_number):
                            calc = Calculation(df, arch, arch_type, comb, year)
                            data = calc.run()
                            strat_db.write_strat(arch, arch_type, year, interval, comb_number, str(comb), data['totalProfit'], data['dealsNumber'], data['profitPercent'], data['avgPercent'], data['minPercent'], data['maxPercent'])


if __name__ == '__main__':
    index = int(sys.argv[1])
    run(TOKEN_LIST[index])
    run(TOKEN_LIST[index+5])