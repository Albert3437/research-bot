import time

TELE_TOKEN = '5667820959:AAHk3L83owZ7AF5-bdItInNkOxNmlDLAx08' # 6583322943:AAH0NHk0V25t502hdnUGbyODyblw30TFfYk
TELE_USER_ID = '476600066'
TOKEN_LIST = ["DOGE", "SOL", "DOT", "AVAX", "ADA", "BTC", "LTC", "ETH", "TRX", 'SHIB']
SIGNAL_LIST = ['ADX', 'Bollinger', 'CCI', 'CMF', 'Ichimoku', 'MACD', 'Momentum', 'OBV', 'SAR', 'ROC', 'RSI', 'SMA', 'Stochastic', 'WPR', 'TR', 'ATR', 'AD', 'AA', 'TS', 'DM', 'PPO', 'PPOP', 'TSI', 'RS', 'ADO', 'MFI']
YEARS = [2022, 2023]
INTERVALS = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h']
ARCH_LIST = ['classic', "classic reverse"]
ARCH_TYPE = ['classic', 'all signals']
COMB_NUMBER_LIST = [1,2,3]
FEES = 0.0005 #Комиссия в процнтах, 100% == 1

# Конфиг для исходных данных

START_DATE = '2022-01-01'
END_DATE = time.time()

# Конфиг для второй части

PROFIT_STRAT_NUMBER = 100
MAX_DEAL_NUMBER = 3000
MIN_TOTAL_PERCENT = 1
DEALS_PROFIT_PERCENT = .65

def INDICATOR_DICT(ta):
    INDICATOR_DICT = {'ADX':ta.average_directional_index,
                        'Bollinger':ta.bollinger_bands,
                        'CCI':ta.commodity_channel_index,
                        'CMF':ta.chaikin_money_flow,
                        'Ichimoku':ta.calculate_ichimoku_cloud,
                        'MACD':ta.macd,
                        'Momentum':ta.calculate_momentum_system,
                        'OBV':ta.on_balance_volume,
                        'SAR':ta.parabolic_sar,
                        'ROC':ta.rate_of_change,
                        'RSI':ta.relative_strength_index,
                        'SMA':ta.moving_average,
                        'Stochastic':ta.stochastic_oscillator,
                        'WPR':ta.williams_percent_range,
                        'TR':ta.TR,
                        'ATR':ta.ATR,
                        'AD':ta.AD,
                        'AA':ta.AA,
                        'TS':ta.TS,
                        'DM':ta.DM,
                        'PPO':ta.PPO,
                        'PPOP':ta.PPOP,
                        'TSI':ta.TSI,
                        'RS':ta.RS,
                        'ADO':ta.ADO,
                        'MFI':ta.MFI}
    return INDICATOR_DICT