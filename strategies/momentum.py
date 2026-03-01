import pandas as pd
import pandas_ta as ta

class MomentumStrategy:
    def analyze(self, df):
        # MACD and EMA crossovers for strong momentum
        df['EMA_9'] = ta.ema(df['close'], length=9)
        df['EMA_21'] = ta.ema(df['close'], length=21)
        
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        if macd is not None:
            df = pd.concat([df, macd], axis=1)
            macd_line = df.columns[df.columns.str.contains('MACD_')][0]
            signal_line = df.columns[df.columns.str.contains('MACDs_')][0]
            
            latest = df.iloc[-1]
            prev = df.iloc[-2]
            
            # Buy signal: MACD crosses above signal, EMA9 crosses above EMA21
            if (latest[macd_line] > latest[signal_line] and prev[macd_line] <= prev[signal_line]) and \
               (latest['EMA_9'] > latest['EMA_21']):
                return 'buy', 2, "Momentum: MACD bullish cross with EMA alignment."
                
            # Sell signal: MACD crosses below signal, EMA9 crosses below EMA21
            elif (latest[macd_line] < latest[signal_line] and prev[macd_line] >= prev[signal_line]) and \
                 (latest['EMA_9'] < latest['EMA_21']):
                return 'sell', -2, "Momentum: MACD bearish cross with EMA alignment."
                
        return 'hold', 0, "Momentum: Neutral"
