import pandas as pd
import pandas_ta as ta

class MeanReversionStrategy:
    def analyze(self, df):
        # RSI, Bollinger Bands for Mean Reversion
        df['RSI'] = ta.rsi(df['close'], length=14)
        bbands = ta.bbands(df['close'], length=20, std=2)
        if bbands is not None:
            df = pd.concat([df, bbands], axis=1)
            lower_band = df.columns[df.columns.str.contains('BBL')][0]
            upper_band = df.columns[df.columns.str.contains('BBU')][0]
            
            latest = df.iloc[-1]
            if latest['close'] < latest[lower_band] and latest['RSI'] < 30:
                return 'buy', 2, "MeanReversion: Price below lower BB and RSI oversold."
            elif latest['close'] > latest[upper_band] and latest['RSI'] > 70:
                return 'sell', -2, "MeanReversion: Price above upper BB and RSI overbought."
        return 'hold', 0, "MeanReversion: Neutral"
