from time import perf_counter
import pandas as pd
from modules.config import *


class Calculation:
    def __init__(self, df:pd.DataFrame, arch:str, arch_type:str, indicator_list:list, bank:int=500):
        self.df = df
        self.arch = arch
        self.type = arch_type
        self.indicator_list = indicator_list
        self.start_sum = bank
        self.keys = list(df.keys())

    
    def calc_metric(self):
        metrics_dict = {'totalProfit':0, 'dealsNumber':0, 'profitPercent':0, 'avgPercent':0, 'minPercent':0, 'maxPercent':0}
        if len(self.percent_list):
            metrics_dict['totalProfit'] = round(self.bank/self.start_sum, 5)
            metrics_dict['dealsNumber'] = round(len(self.percent_list), 5)
            profit_percent = 0
            for percent in self.percent_list:
                if percent >= 1:
                    profit_percent += 1
            metrics_dict['profitPercent'] = round(profit_percent/len(self.percent_list), 5)
            metrics_dict['avgPercent'] = round(sum(self.percent_list) / len(self.percent_list) if self.percent_list else 0, 5)
            metrics_dict['minPercent'] = round(min(self.percent_list), 5)
            metrics_dict['maxPercent'] = round(max(self.percent_list), 5)
        return metrics_dict


    def calc_bank(self, close, side):
        if (self.ans[0] == -1 and self.type == 'all signals') or (self.ans[0] == -1 and side == 1 and self.type == 'classic'):
            percent = self.price/close
            self.bank *= percent - FEES
            self.percent_list.append(percent)
            self.switcher=0
        elif (self.ans[0] == 1 and self.type == 'all signals') or (self.ans[0] == 1 and side == -1 and self.type == 'classic'):
            percent = close/self.price
            self.bank *= percent - FEES
            self.percent_list.append(percent)
            self.switcher=0
        self.ans = side, close
        if self.switcher == 0:
            self.price = close
            self.switcher=1



    def core(self, row):
        pos_side = 0
        signals = set()
        for sign in self.indicator_list:
            indicator_index = self.keys.index(f'{sign} signal') 
            signals.add(row[indicator_index])
        if len(signals) == 1:
            pos_side = signals.pop()

        return  pos_side
    

    def run(self):
        self.switcher = 0
        self.bank = self.start_sum
        self.ans = ['', '']
        self.percent_list = []
        array = self.df.to_numpy()


        if self.arch == "classic":
            for row in array:
                side = self.core(row)
                close = float(row[4])
                if side != 0:
                    self.calc_bank(close, side)

        elif self.arch == "classic reverse":
            for row in array:
                side = self.core(row) * -1
                close = float(row[4])
                if side != 0:
                    self.calc_bank(close, side)

        return self.calc_metric()


                
        



#df = pd.read_csv('data/ADAUSDT/data_2022/1m.csv')\

#from modules.indicators import TechnicalIndicators
#ta = TechnicalIndicators(df)
#
#for values in INDICATOR_DICT.values():
#    eval(values)
#
#start = perf_counter()
#calc = Calculation(df, 'classic', 'all signals', ['ADX'])
#print(calc.run())
#print('time', (perf_counter() - start))