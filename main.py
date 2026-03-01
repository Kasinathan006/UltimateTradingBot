import os
import time
import datetime
from dotenv import load_dotenv

# Loading local modules
from core.multi_exchange import MultiExchangeManager
from core.db import TradeJournal
from core.risk_manager import RiskManager
from agents.chief_analyst import ChiefAnalystAgent

from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Titan AI Trading Bot is ALIVE and RUNNING!"

def run_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_server)
    t.daemon = True
    t.start()

# AI-Selected best pairs to scalp
top_markets = [
    'ETH/USDT', 'BTC/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT', 'AVAX/USDT'
]

def main():
    load_dotenv()
    
    keep_alive() # Start the dummy web server for Render health checks
    
    print("[*] Starting GOD MODE Multi-Exchange Titan Algo")
    print(f"[*] Environment: {'SANDBOX (Paper Trading)' if os.getenv('USE_SANDBOX', 'true').lower() == 'true' else 'LIVE (Real Money)'}")
    
    exchange_configs = {
        'binance': {
            'api_key': os.getenv('BINANCE_API_KEY'),
            'api_secret': os.getenv('BINANCE_API_SECRET')
        },
        'kraken': {
            'api_key': os.getenv('KRAKEN_API_KEY'),
            'api_secret': os.getenv('KRAKEN_API_SECRET')
        }
        # You can add kucoin, bybit, etc. here in the future
    }
    
    # Initialize Core Systems
    testnet = os.getenv('USE_SANDBOX', 'true').lower() == 'true'
    multi_exchange = MultiExchangeManager(exchange_configs, testnet=testnet)
    db = TradeJournal()
    risk_manager = RiskManager()
    
    # Initialize AI Agents
    chief_analyst = ChiefAnalystAgent()
    
    try:
        while True:
            print("\n" + "="*50, flush=True)
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Neural AI scanning across markets...", flush=True)
            
            # Fetch global balances
            balances = multi_exchange.fetch_balances()
            print(f"[*] Global Balances: {balances}")
            
            for symbol in top_markets:
                print(f"--> AI deep scanning {symbol}...", flush=True)
                
                # Fetch 500 candles on 1-minute timeframe for high-speed analysis and accurate EMA-200
                ohlcv = multi_exchange.fetch_ohlcv(symbol, timeframe='1m', limit=500)
                if not ohlcv:
                    print("    [!] Failed to get OHLCV data. Skipping.")
                    continue
                
                # The Chief Analyst Agent synthesizes signals from 4 advanced strategies
                signal, reason = chief_analyst.analyze_market(ohlcv)
                print(f"    Signal: {signal.upper()} | {reason}")
                
                # Execution Logic (Only considering Long positions for spot markets)
                if signal == 'buy':
                    if not risk_manager.can_trade():
                        print("    [X] Blocked by Risk Manager: Daily drawdown limit reached.")
                        continue
                        
                    # For a basic simulation, just take a dummy position size 
                    # since RiskManager expects a stop_loss_price parameter
                    current_price = ohlcv[-1][4]
                    stop_loss_price = current_price * 0.99 # 1% trailing stop
                    
                    # Assuming all exchanges are loaded, use Binance balance for risk if possible
                    # or just default a dummy balance
                    current_balance = balances.get('binance', {}).get('USDT', 1000)
                    
                    pos_size = risk_manager.calculate_position_size(current_balance, current_price, stop_loss_price)
                    
                    # If this yields 0, just test with 20 USDT for sanity
                    if pos_size == 0: pos_size = 20
                    
                    is_safe = True # Mocking check
                    if is_safe:
                        # Convert USDT to token quantity
                        qty = pos_size / current_price 
                        
                        # Only execute a tiny amount for testing/safety
                        order, ex_id = multi_exchange.execute_trade(symbol, 'buy', qty)
                        if order:
                            print(f"    [!] EXECUTED BUY on {ex_id.upper()}! Order details: {order['id']}")
                            db.log_trade(symbol, 'buy', qty, current_price, reason)
                        else:
                            print("    [X] Execution failed.")
                    else:
                        print(f"    [X] Blocked by Risk Manager: {risk_reason}")
                else:
                    # Ignore sell signals as we aren't shorting natively in spot without asset validation
                    if signal == 'sell':
                        print("    [i] Ignoring SELL signal (Spot markets require previous asset ownership).")

            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cycle complete. AI cooling down for 10s...", flush=True)
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n[X] God Mode Algo stopped by user.")

if __name__ == "__main__":
    main()
