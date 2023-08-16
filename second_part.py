from modules.prepare_data import get_combinations
from modules.config import *
from modules.logger import logger
import json
import pandas as pd




@logger.catch
def json_load(filename):
    with open(f'{filename}.json', 'r') as f:
        data = json.load(f)
    return data


@logger.catch
def amount_filter(amount_dict): 
    keys_to_remove=[]
    for key, value in amount_dict.items():
        if value['dealsNumber'] > 3000:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del amount_dict[key]
    return amount_dict


@logger.catch
def create_balance_dict(amount_dict):
    balance_dict = {}
    for key, value in amount_dict.items():
        balance_dict[key] = value['totalProfit']
    return balance_dict


@logger.catch
def create_full_dict(sorted_dict, amount_dict):
    ready_dict = {}
    for key, _ in sorted_dict.items():
        ready_dict[key] = amount_dict[key]
    return ready_dict


@logger.catch
def calculate(data):
    amount_dict = {}
    for arch in ARCH_LIST:
        for arch_type in ARCH_TYPE:
            for year in 2023:
                for interval in INTERVALS:
                    for comb_number in COMB_NUMBER_LIST:
                        for comb in get_combinations(comb_number):
                            amount = data[arch][arch_type][year][interval][comb_number][comb]
                            amount_dict[arch,arch_type,year,interval,comb_number,comb] = amount
    
    amount_dict = amount_filter(amount_dict)

    balance_dict = create_balance_dict(amount_dict)

    sorted_number = int(len(balance_dict)*0.2)
    sorted_dict = dict(sorted(balance_dict.items(), key=lambda item: item[1], reverse=True)[:sorted_number])
    
    ready_dict = create_full_dict(sorted_dict, amount_dict)

    return ready_dict


@logger.catch
def run():
    finaly_data = []
    for i, token in enumerate(TOKEN_LIST):
        calculate_data = json_load(token)
        calculated_data = calculate(calculate_data)
        for key, data in calculated_data[i].items():
            ready_data = {'token':token}
            ready_data['arch'] = key[0]
            ready_data['arch_type'] = key[1]
            ready_data['year'] = key[2]
            ready_data['interval'] = key[3]
            ready_data['comb_number'] = key[4]
            ready_data['comb'] = key[5]
            for key, value in data.items():
                ready_data[key] = value
            finaly_data.append(ready_data)
    df = pd.DataFrame(finaly_data)
    df.to_excel('analized.xlsx')