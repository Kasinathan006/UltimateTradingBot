import ccxt
import time

class ExchangeManager:
    def __init__(self, exchange_id, api_key, api_secret, testnet=True):
        self.exchange_class = getattr(ccxt, exchange_id)
        self.exchange = self.exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,
        })
        
        if testnet:
            if 'test' in self.exchange.urls:
                self.exchange.urls['api'] = self.exchange.urls['test']
            else:
                print(f"Warning: {exchange_id} does not have a Sandbox URL listed. Using live.")
                
        self.exchange.load_markets()

    def fetch_ohlcv(self, symbol, timeframe='1h', limit=100):
        try:
            bars = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            return bars
        except Exception as e:
            print(f"Error fetching OHLCV mapping: {e}")
            return None

    def place_market_order(self, symbol, side, amount):
        if not self.exchange.apiKey:
            print(f"[DEMO/PAPER] Simulated Order Placed: {side.upper()} {amount} {symbol}")
            return {'id': 'mock_order_123', 'info': {}, 'status': 'closed'}
        try:
            order = self.exchange.create_market_order(symbol, side, amount)
            return order
        except Exception as e:
            print(f"Failed to place order: {e}")
            return None

    def fetch_balance(self):
        if not self.exchange.apiKey:
            return {'total': {'USDT': 10000}} # Fake paper trading balance
        try:
            return self.exchange.fetch_balance()
        except Exception as e:
            print(f"[!] Balance fetch failed, defaulting to 10k: {e}")
            return {'total': {'USDT': 10000}}
