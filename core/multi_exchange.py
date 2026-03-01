import ccxt
import time

class MultiExchangeManager:
    """
    Manages connections and operations across multiple cryptocurrency exchanges simultaneously.
    """
    def __init__(self, exchange_configs, testnet=True):
        self.exchanges = {}
        for ex_id, config in exchange_configs.items():
            try:
                ex_class = getattr(ccxt, ex_id)
                exchange = ex_class({
                    'apiKey': config.get('api_key', ''),
                    'secret': config.get('api_secret', ''),
                    'enableRateLimit': True,
                })
                
                # Setup Sandbox/Testnet if required
                if testnet:
                    if 'test' in exchange.urls:
                        exchange.urls['api'] = exchange.urls['test']
                    else:
                        print(f"[!] Warning: {ex_id} does not support Sandbox. Connecting to LIVE.")
                
                exchange.load_markets()
                self.exchanges[ex_id] = exchange
                print(f"[+] Successfully connected to {ex_id.upper()}")
            except Exception as e:
                print(f"[-] Failed to load exchange {ex_id}: {e}")

    def get_supported_exchanges(self, symbol):
        """Returns a list of exchange IDs that support the given trading pair."""
        supported = []
        for ex_id, ex in self.exchanges.items():
            if symbol in ex.markets:
                supported.append(ex_id)
        return supported

    def fetch_ohlcv(self, symbol, timeframe='1m', limit=200):
        """Fetches OHLCV from the first exchange that supports it."""
        for ex_id, ex in self.exchanges.items():
            try:
                if symbol in ex.markets:
                    return ex.fetch_ohlcv(symbol, timeframe, limit=limit)
            except Exception:
                continue
        return None

    def execute_trade(self, symbol, side, amount, preferred_exchange=None):
        """Executes a trade on the preferred exchange or the first available one."""
        ex_ids = [preferred_exchange] if preferred_exchange and preferred_exchange in self.exchanges else list(self.exchanges.keys())
        
        for ex_id in ex_ids:
            ex = self.exchanges.get(ex_id)
            if ex and symbol in ex.markets:
                if not ex.apiKey:
                    print(f"[{ex_id.upper()} PAPER/MOCK] Executed {side.upper()} {amount} of {symbol}")
                    return {'id': f'mock_{int(time.time())}', 'info': {}, 'status': 'closed'}, ex_id
                
                try:
                    order = ex.create_market_order(symbol, side, amount)
                    return order, ex_id
                except Exception as e:
                    print(f"[X] Execution failed on {ex_id}: {e}")
        return None, None

    def fetch_balances(self):
        """Returns a compiled dictionary of USDT balances across all exchanges."""
        balances = {}
        for ex_id, ex in self.exchanges.items():
            if not ex.apiKey:
                balances[ex_id] = {'USDT': 10000} # Mock balance
                continue
            
            try:
                bal = ex.fetch_balance()
                balances[ex_id] = bal.get('total', {})
            except Exception as e:
                balances[ex_id] = {'USDT': 10000}
                print(f"[X] Balance fetch failed on {ex_id}: {e}")
                
        return balances
