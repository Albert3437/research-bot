import pandas as pd
from modules.indicators import TechnicalIndicators
from modules.logger import logger
from modules.config import *
from numba import jit


class Calculation:
    def __init__(self, df:pd.DataFrame, arch:str, arch_type:str, indicator_list:list, token:str, interval:str, year:int, bank:int=500):
        self.arch = arch
        self.type = arch_type
        self.indicator_list = indicator_list
        self.start_sum = bank
        self.df = df


    @logger.catch
    def calculate(self, df, signal_list):
            # Вычисление необходимых индикаторов
            ta = TechnicalIndicators(df)
            
            for signal in signal_list:
                eval(INDICATOR_DICT[signal])
            return df


    @logger.catch
    def core(self, df, indicator_list):
        pos_side = 0
        signals = set()
        for sign in indicator_list:
            signals.add(df[f'{sign} signal'])
        if len(signals) == 1:
            pos_side = signals.pop()
        
        return  pos_side


    @logger.catch
    def calc_metric(self):
        metrics_dict = {'totalProfit':0, 'dealsNumber':0, 'profitPercent':0, 'avgPercent':0, 'minPercent':0, 'maxPercent':0}
        if len(self.percent_list):
            metrics_dict['totalProfit'] = round(self.bank / self.start_sum, 5)
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


    @logger.catch
    def calc_bank(self, close, side):
        if (self.ans[0] == -1 and self.type == 'all signals') or (self.ans[0] == -1 and side != self.ans[0] and self.type == 'classic'):
            percent = self.price/close
            self.bank *= percent - FEES
            self.percent_list.append(percent)
            self.switcher=0
        elif (self.ans[0] == 1 and self.type == 'all signals') or (self.ans[0] == 1 and side != self.ans[0] and self.type == 'classic'):
            percent = close/self.price
            self.bank *= percent - FEES
            self.percent_list.append(percent)
            self.switcher=0
        self.ans = side, close
        if self.switcher == 0:
            self.price = close
            self.switcher=1


    @logger.catch
    def run(self):
        self.switcher = 0
        self.bank = self.start_sum
        self.ans = ['', '']
        self.percent_list = []
        if self.arch == "classic":
            #self.df = self.calculate(self.df, self.indicator_list)

            for _, row in self.df.iterrows():
                close = float(row['close'])
                side = self.core(row, self.indicator_list)

                if side == 1:
                    self.calc_bank(close, side)
                if side == -1:
                    self.calc_bank(close, side)

        elif self.arch == "classic reverse":
            #self.df = self.calculate(self.df, self.indicator_list)

            for _, row in self.df.iterrows():
                close = float(row['close'])
                side = self.core(row, self.indicator_list)

                if side == 1:
                    self.calc_bank(close, side)
                if side == -1:
                    self.calc_bank(close, side)
        
        return self.calc_metric()


#calc = Calculation('classic', 'all signals', ['WPR'], 'ADA', '1m', 2023, 500)
#print(calc.run())