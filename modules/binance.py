from binance.client import Client
import pandas as pd
import time
from modules.logger import logger


class BinanceData:
    def __init__(self, api_key='API_KEY', api_secret='API_SECRET'):
        self.client = Client(api_key, api_secret)

    logger.catch
    def get_historical_candles(self, start_date, end_date, symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_5MINUTE):
        while True:
            # Цикл нужен для того чтобы при проблемах с ответами сервера(такое было), была повторная попытка получния свечей
            try:
                # Получение исторических данных для тестов стратегии
                candles = self.client.get_historical_klines(f'{symbol}USDT', interval, str(start_date), str(end_date))
                columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']  # список нужных столбцов
                df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
                df = df[columns]
                return df
            except Exception as e:
                logger.error(e)
                time.sleep(5)

    logger.catch
    def get_last_candles(self, limit=100, symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_5MINUTE):
        # Получение актуальных 5-ти минутных свечей
        while True:
            # Цикл нужен для того чтобы при проблемах с ответами сервера(такое было), была повторная попытка получния свечей
            try:
                candles = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
                columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
                df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
                df = df[columns]
                return df  # Выходим из цикла при успешном выполнении
            except Exception as e:
                logger.error(e)
                time.sleep(5)

    