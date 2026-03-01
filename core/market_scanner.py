import pandas as pd
import pandas_ta as ta

class MarketScanner:
    def __init__(self, exchange_manager):
        self.em = exchange_manager

    def get_top_tradable_pairs(self, limit=10, min_volume_usd=1000000):
        print("[*] Scanning market for the best opportunities...")
        try:
            markets = self.em.exchange.load_markets()
            tickers = self.em.exchange.fetch_tickers()
            
            valid_pairs = []
            for symbol, ticker in tickers.items():
                # Filter for USDT pairs, active markets, and avoid leveraged tokens (e.g., BULL/BEAR)
                if '/USDT' in symbol and ':' not in symbol and 'UP/' not in symbol and 'DOWN/' not in symbol:
                    quote_volume = ticker.get('quoteVolume', 0)
                    if quote_volume and quote_volume > min_volume_usd:
                        valid_pairs.append({
                            'symbol': symbol,
                            'volume': quote_volume,
                            'change': ticker.get('percentage', 0)
                        })
            
            # Sort by highest volume and volatility (absolute percentage change)
            df = pd.DataFrame(valid_pairs)
            if df.empty:
                return []
                
            df['volatility_score'] = abs(df['change']) * df['volume']
            df = df.sort_values(by='volatility_score', ascending=False)
            
            top_pairs = df.head(limit)['symbol'].tolist()
            print(f"[*] AI Selected Top Markets to analyze: {top_pairs}")
            return top_pairs
        except Exception as e:
            print(f"Error scanning markets: {e}")
            return ["BTC/USDT", "ETH/USDT"] # Fallback

    def analyze_trend(self, symbol):
        # Quick pre-scan to see if a market is trending
        ohlcv = self.em.fetch_ohlcv(symbol, timeframe='1d', limit=14)
        if not ohlcv:
            return 0
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['ADX'] = ta.adx(df['high'], df['low'], df['close'], length=14)['ADX_14']
        
        current_adx = df['ADX'].iloc[-1]
        return current_adx if not pd.isna(current_adx) else 0
