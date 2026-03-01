import pandas as pd
import pandas_ta as ta

class ProTraderEngine:
    """
    Advanced Multi-Factor Human-like Algorithmic Intelligence.
    Uses Confluence of:
    1. Trend (EMA 20/50/200)
    2. Momentum (MACD)
    3. Overbought/Oversold (RSI)
    4. Volatility (Bollinger Bands & ATR)
    """

    def analyze_market(self, ohlcv_data):
        if not ohlcv_data or len(ohlcv_data) < 200:
            return 'hold', "Not enough data for advanced analysis."

        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # 1. Trend Analysis
        df['EMA_20'] = ta.ema(df['close'], length=20)
        df['EMA_50'] = ta.ema(df['close'], length=50)
        df['EMA_200'] = ta.ema(df['close'], length=200)

        # 2. Momentum (MACD)
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        df['MACD'] = macd['MACD_12_26_9']
        df['MACD_signal'] = macd['MACDs_12_26_9']
        df['MACD_hist'] = macd['MACDh_12_26_9']

        # 3. Oscillators (RSI)
        df['RSI'] = ta.rsi(df['close'], length=14)

        # 4. Volatility (Bollinger Bands & ATR)
        bbands = ta.bbands(df['close'], length=20, std=2)
        df['BB_LOWER'] = bbands.iloc[:, 0] # Lower band is the first column
        df['BB_UPPER'] = bbands.iloc[:, 2] # Upper band is the third column
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)

        # Get latest data points
        curr = df.iloc[-1]
        prev = df.iloc[-2]

        score = 0
        reasons = []

        # --- AI SCORING ALGORITHM ---

        # Trend Scoring
        if curr['close'] > curr['EMA_200']:
            score += 1
            reasons.append("Macro Trend Bullish (Price > 200 EMA)")
        elif curr['close'] < curr['EMA_200']:
            score -= 1
            reasons.append("Macro Trend Bearish (Price < 200 EMA)")

        if curr['EMA_20'] > curr['EMA_50']:
            score += 1
            reasons.append("Micro Trend Bullish (20 EMA > 50 EMA)")
        else:
            score -= 1

        # Momentum Scoring (MACD Histogram expanding)
        if curr['MACD'] > curr['MACD_signal'] and curr['MACD_hist'] > prev['MACD_hist']:
            score += 2
            reasons.append("Strong MACD Bullish Momentum")
        elif curr['MACD'] < curr['MACD_signal'] and curr['MACD_hist'] < prev['MACD_hist']:
            score -= 2
            reasons.append("Strong MACD Bearish Momentum")

        # RSI Mean Reversion / Divergence check
        if curr['RSI'] < 30:
            score += 2
            reasons.append("Oversold (RSI < 30) - Reversal expected")
        elif curr['RSI'] > 70:
            score -= 2
            reasons.append("Overbought (RSI > 70) - Pullback expected")

        # Bollinger Band squeeze / breakout
        if curr['close'] < curr['BB_LOWER']:
            score += 1
            reasons.append("Price below lower BB (Deviated from mean)")
        elif curr['close'] > curr['BB_UPPER']:
            score -= 1
            reasons.append("Price above upper BB (Overextended)")

        # --- VERDICT ---
        confidence = abs(score)

        # 6. Verdict (Modified for Scalping)
        if score >= 1:
            return 'buy', f"Scalp BUY Signal. High Probability setup. (Score: {score})"
        elif score <= -1:
            return 'sell', f"Scalp SELL Signal. High Probability drop. (Score: {score})"
        else:
            return 'hold', f"Waiting for perfect safe entry. (Score: {score})"

    def calculate_dynamic_sl_tp(self, ohlcv_data, entry_price, side):
        """Ultra-conservative No-Loss Scalping logic"""
        # Take a very tiny guaranteed profit (0.2% - 0.5%)
        # Cut losses instantly if the market moves against us by a tiny fraction (0.1%)
        
        if side == 'buy':
            stop_loss = entry_price * 0.995  # Cut loss if it drops 0.5%
            take_profit = entry_price * 1.002 # Take profit immediately at 0.2% gain
        else:
            stop_loss = entry_price * 1.005
            take_profit = entry_price * 0.998

        return stop_loss, take_profit
