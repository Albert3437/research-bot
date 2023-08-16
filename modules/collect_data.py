from modules.binance import BinanceData
from modules.config import INTERVALS, TOKEN_LIST
import time


def update_data():

    bd = BinanceData()
    dates = [['2021-01-01','2021-12-31'], ['2022-01-01','2022-12-31'], ['2023-01-01',time.time()*1000]]
    for symbol in TOKEN_LIST:
        print(symbol)
        for date in dates:
            print(date) 
            for interval in INTERVALS:
                print(interval)

                df = bd.get_historical_candles(symbol=symbol, start_date=date[0], end_date=date[1], interval=interval)
                
                df.to_csv(f'data/{symbol}USDT/data_{date[:4]}/{interval}.csv', index=False)
