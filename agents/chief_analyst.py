import pandas as pd

from strategies.pro_trader_engine import ProTraderEngine
from strategies.mean_reversion import MeanReversionStrategy
from strategies.volatility_breakout import VolatilityBreakoutStrategy
from strategies.momentum import MomentumStrategy

class ChiefAnalystAgent:
    """
    Acts as the Head of Trading. It queries multiple specialized sub-strategies/agents
    and aggregates their confidence scores to make an ultra-high-conviction decision.
    """
    def __init__(self):
        self.pro_trader = ProTraderEngine()
        self.mean_reverter = MeanReversionStrategy()
        self.breakout_hunter = VolatilityBreakoutStrategy()
        self.momentum_tracker = MomentumStrategy()
        
    def analyze_market(self, ohlcv_data):
        if not ohlcv_data or len(ohlcv_data) < 200:
            return 'hold', "Not enough data for multi-agent synthesis."
            
        df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Gather votes from all strategies
        total_score = 0
        reasons = []
        
        # Strategy 1: The original Pro Trader Engine
        sig1, reason1 = self.pro_trader.analyze_market(ohlcv_data)
        if sig1 == 'buy': total_score += 1
        elif sig1 == 'sell': total_score -= 1
        if sig1 != 'hold': reasons.append(reason1)
        
        # Strategy 2: Mean Reversion
        sig2, score2, reason2 = self.mean_reverter.analyze(df.copy())
        total_score += score2
        if sig2 != 'hold': reasons.append(reason2)
            
        # Strategy 3: Volatility Breakout
        sig3, score3, reason3 = self.breakout_hunter.analyze(df.copy())
        total_score += score3
        if sig3 != 'hold': reasons.append(reason3)
            
        # Strategy 4: Momentum
        sig4, score4, reason4 = self.momentum_tracker.analyze(df.copy())
        total_score += score4
        if sig4 != 'hold': reasons.append(reason4)
            
        # Decision Synthesis (Consensus)
        # Max positive score = 1 (Pro) + 2 (Mean) + 2 (Break) + 2 (Mom) = 7
        # We demand a strong consensus score of >= 3 for a trade
        
        final_reason = " | ".join(reasons) if reasons else "Waiting for consensus."
        
        if total_score >= 3:
            return 'buy', f"Strong BUY Consensus (Score: {total_score}). Logic: {final_reason}"
        elif total_score <= -3:
            return 'sell', f"Strong SELL Consensus (Score: {total_score}). Logic: {final_reason}"
            
        return 'hold', f"Mixed/Weak signals (Score: {total_score}). Staying out."
