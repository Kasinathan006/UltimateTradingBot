import pandas as pd
import pandas_ta as ta

class TrendFollowingStrategy:
    def __init__(self, short_ema=9, long_ema=21):
        self.short_ema = short_ema
        self.long_ema = long_ema

    def generate_signal(self, ohlcv_data):
        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['EMA_short'] = ta.ema(df['close'], length=self.short_ema)
        df['EMA_long'] = ta.ema(df['close'], length=self.long_ema)
        
        # Latest values
        curr_short = df['EMA_short'].iloc[-1]
        curr_long = df['EMA_long'].iloc[-1]
        prev_short = df['EMA_short'].iloc[-2]
        prev_long = df['EMA_long'].iloc[-2]

        # Golden Cross (Bullish) - Short crosses Long upwards
        if prev_short <= prev_long and curr_short > curr_long:
            return 'buy', "Golden Cross: Short EMA crossed above Long EMA"
        
        # Death Cross (Bearish) - Short crosses Long downwards
        elif prev_short >= prev_long and curr_short < curr_long:
            return 'sell', "Death Cross: Short EMA crossed below Long EMA"
            
        return 'hold', "No trend crossover signal"
