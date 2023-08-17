from modules.config import *
from calculate import Calculation
import json
from modules.logger import logger
from modules.telegram import Telegram
from modules.prepare_data import get_combinations

@logger.catch
def json_dump(data, filename):
    with open(f'{filename}.json', 'w') as f:
        json.dump(data, f)



@logger.catch
def run(token):
    telega = Telegram()
    telega.send_message(token)
    arch_dict = {}
    for arch in ARCH_LIST:
        arch_type_dict = {}
        for arch_type in ARCH_TYPE:
            year_type_dict = {}
            for year in YEARS:
                telega.send_message(year)
                interval_dict = {}
                for interval in INTERVALS:
                    telega.send_message(interval)
                    comb_number_dict = {}
                    for comb_number in COMB_NUMBER_LIST:
                        telega.send_message(str((token, comb_number)))
                        comb_dict = {}
                        for comb in get_combinations(comb_number):
                            telega.send_message(str((token, comb)))
                            calc = Calculation(arch, arch_type, comb, token, interval, year)
                            data = calc.run()
                            comb_dict[tuple(comb)] = data
                        comb_number_dict[comb_number] = comb_dict
                    interval_dict[comb_number] = comb_dict
                year_type_dict[comb_number] = comb_dict
            arch_type_dict[comb_number] = comb_dict
        arch_dict[comb_number] = comb_dict
    json_dump(arch_dict, token)
    return arch_dict


