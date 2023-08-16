from modules.logger import logger
from modules.config import *

@logger.catch
def get_combinations(comb_number):
    indicator_list = []
    for i1, indicator1 in enumerate(SIGNAL_LIST):
        if comb_number == 1:
            indicator_list.append([indicator1])
        for i2, indicator2 in enumerate(SIGNAL_LIST):
            if comb_number == 2:
                if i1 < i2:
                    indicator_list.append([indicator1, indicator2])
            for i3, indicator3 in enumerate(SIGNAL_LIST):
                if comb_number == 3:
                    if i1 < i2 < i3:
                        indicator_list.append([indicator1, indicator2, indicator3])
    return indicator_list