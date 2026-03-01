class RiskManager:
    def __init__(self, max_risk_percentage=1.0, max_drawdown=10.0):
        self.max_risk_percentage = max_risk_percentage  # Risk only 1% of total portfolio per trade
        self.max_drawdown = max_drawdown
        self.daily_loss = 0

    def calculate_position_size(self, current_balance, current_price, stop_loss_price):
        """
        Position Size = (Account Risk) / (Trade Risk)
        eg. $10,000 account, 1% risk = $100 max loss.
        Entry: $50,000. SL: $49,000 (1000 diff). 
        Size = 100 / 1000 = 0.1 BTC.
        """
        risk_amount = current_balance * (self.max_risk_percentage / 100)
        price_difference = abs(current_price - stop_loss_price)
        
        if price_difference == 0:
            return 0
            
        size = risk_amount / price_difference
        return size

    def can_trade(self):
        # Kill switch if drawdown hits max threshold
        if self.daily_loss >= self.max_drawdown:
            return False
        return True
