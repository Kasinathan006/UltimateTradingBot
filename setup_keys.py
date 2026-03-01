import os

def setup():
    print("="*60)
    print("🤖 GOD MODE BOT - SECURE API CONFIGURATION 🤖")
    print("="*60)
    print("Please paste your keys below. This is entirely local.")
    print("Your keys will be saved securely to the '.env' file.\n")

    api_key = input("Enter your Binance API Key: ").strip()
    api_secret = input("Enter your Binance API Secret: ").strip()
    
    print("\n[Optional] Enter your Telegram details for live trade alerts.")
    telegram_token = input("Enter Telegram Bot Token (or press Enter to skip): ").strip()
    chat_id = input("Enter Telegram Chat ID (or press Enter to skip): ").strip()

    env_content = f"""# Exchange Configuration
EXCHANGE_ID=binance
API_KEY={api_key}
API_SECRET={api_secret}

# Mode Configuration (False means LIVE trading with REAL MONEY)
TESTNET=False

# Telegram Alerts
TELEGRAM_TOKEN={telegram_token}
TELEGRAM_CHAT_ID={chat_id}
"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    with open(env_path, 'w') as f:
        f.write(env_content)
        
    print("\n✅ Configuration saved securely to '.env'!")
    print("You are now ready to unleash the bot on the live market.")
    print("To start the bot, run: python main.py")
    
if __name__ == "__main__":
    setup()
