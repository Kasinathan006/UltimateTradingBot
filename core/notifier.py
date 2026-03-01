import requests

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, message):
        if not self.bot_token or not self.chat_id:
            print(f"Telegram Config missing: {message}")
            return
            
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Error sending Telegram message: {e}")

    def send_alert(self, symbol, side, amount, price, reason):
        msg = f"🚨 *TRADE ALERT* 🚨\n\n*Symbol:* {symbol}\n*Action:* {side.upper()}\n*Amount:* {amount}\n*Price:* {price}\n*Reason:* {reason}"
        self.send_message(msg)
