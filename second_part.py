from modules.prepare_data import get_combinations
from modules.config import *
from modules.logger import logger
import pandas as pd
from modules.db import StratsDataBase


@logger.catch
def amount_filter(strats:list):
    strat_list = []
    for i,strat in enumerate(strats):
        if strat['dealsNumber'] < 3000:
            strat_list.append(strats[i])
    return strat_list


@logger.catch
def year_filter(strats):
    strat_list = []
    for strat in strats:
        if strat['year'] == 2023:
            strat_list.append(strat)
    return strat_list


@logger.catch
def non_profit_filter(strats:list):
    strat_list = []
    for i,strat in enumerate(strats):
        if strat['totalProfit'] > 1:
            strat_list.append(strats[i])
    return strat_list


@logger.catch
def profitable_strats(strats):
    best_strats = []
    profit_percents = []
    for strat in strats:
        profit_percents.append(strat['totalProfit'])
    sorted_list = sorted(profit_percents)
    for profit_percent in sorted_list[-20:]:
        index = profit_percents.index(profit_percent)
        best_strats.append(strats[index])
    return best_strats


@logger.catch
def core(token):
    strat_db = StratsDataBase(token)
    strats = strat_db.read_strats()
    strats = non_profit_filter(strats)
    strats = amount_filter(strats)
    strats = year_filter(strats)
    df = pd.DataFrame(strats)
    df['totalProfit'] = df['totalProfit'] * 100
    df.to_excel(f'ready_data/{token}.xlsx')
    strat_db.close_db()
    return strats


@logger.catch
def add_latest_year(strats):
    strat_list = []
    for strat in strats:
        strat_db = StratsDataBase(strat['token'])
        full_strats = strat_db.read_strats()
        for year in YEARS:
            if year != strat['year']:
                for latest_strat in full_strats:
                    if strat['arch'] == latest_strat['arch'] and strat['arch_type'] == latest_strat['arch_type'] and year == latest_strat['year'] and strat['interval'] == latest_strat['interval'] and strat['comb'] == latest_strat['comb']:
                        strat['latestYear'] = year
                        strat['latestYearProfit'] = latest_strat['totalProfit']
                        strat_list.append(strat)
    strat_db.close_db()
    return strat_list

@logger.catch
def run():
    all_data = []
    for token in TOKEN_LIST:
        for strat in core(token):
            strat['token'] = token
            all_data.append(strat)
    data = profitable_strats(all_data)
    data = add_latest_year(data)
    df = pd.DataFrame(data)
    df.to_excel('analized.xlsx')


if __name__ == '__main__':
    run()