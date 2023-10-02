from modules.indicators import TechnicalIndicators
import pandas as pd
import matplotlib.pyplot as plt
from modules.config import INDICATOR_DICT
from modules.binance import BinanceData

def test(df, indicators):
    # Расчет индикаторов
    ta = TechnicalIndicators(df)
    for indicator in indicators:
        eval(INDICATOR_DICT[indicator])

    a=0
    bank = 500
    ans = ['','']
    bank_history = []
    price_history = []
    percent_history = []
    for i in range(len(df)):
        pos_side=0
        signals = set()
        for indicator in indicators:
            signal1 = df[f'{indicator} signal'].iloc[i]
            signals.add(signal1)

        close = float(df['close'].iloc[i])
        timestamp = float(df['timestamp'].iloc[i])

        if len(signals) == 1:
            pos_side = signals.pop()

        if pos_side == 1:
            if ans[0] == -1:
                percent = price/close
                bank *= percent
                bank_history.append(bank)
                price_history.append(close)
                percent_history.append(percent)
                a=0
            ans = 1, close
            if a == 0:
                price = close
                a=1
        elif pos_side == -1:
            if ans[0] == 1:
                percent = close/price
                bank *= percent
                bank_history.append(bank)
                price_history.append(close)
                percent_history.append(percent)
                a=0
            ans = -1, close
            if a == 0:
                price = close
                a=1



    plt.plot(bank_history)
    plt.ylabel('Банк')
    plt.twinx()
    #plt.savefig(f'{sign1} {sign2} {sign3}.png')
    plt.show()
    print('Максимальный:', round(max(percent_history),2), '%')
    print('Минимальный:', round(min(percent_history),2), '%')
    print('Общее среднее:', round((sum(percent_history) / len(percent_history)),4), '%')
    profit_list = []
    lose_list = []
    for profit in percent_history:
        if profit >= 1:
            profit_list.append(profit)
    for lose in percent_history:
        if lose < 1:
            lose_list.append(lose)
    print('Доход среднее:', round((sum(percent_history) / len(percent_history)),4), '%')
    print('Потери среднее:', round((sum(percent_history) / len(percent_history)),4), '%')
    print('Общее количество сделок', len(percent_history))
    print('Профит количество сделок', len(profit_list))
    print('Потери количество сделок', len(lose_list))
    return round(bank, 2)
    

df = pd.read_csv('data/DOTUSDT/data_2023/2h.csv')
value = test(df, ['CCI', 'AD', 'DM'])
print("Общий доход:", value)