import pandas as pd
import pandas_ta as ta

class VolatilityBreakoutStrategy:
    def analyze(self, df):
        # ATR and Donchian Channels (simulated with rolling high/low) for Breakout
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)
        df['Highest20'] = df['high'].rolling(window=20).max()
        df['Lowest20'] = df['low'].rolling(window=20).min()
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        if latest['close'] >= prev['Highest20'] and latest['ATR'] > df['ATR'].mean():
            return 'buy', 2, "Breakout: Price broke 20-period high with high volatility."
        elif latest['close'] <= prev['Lowest20'] and latest['ATR'] > df['ATR'].mean():
            return 'sell', -2, "Breakout: Price broke 20-period low with high volatility."
        
        return 'hold', 0, "Breakout: Neutral"
