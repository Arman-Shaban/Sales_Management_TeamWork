from models.order import Order

class Bank:
    def __init__(self, balance):
        self.balance = balance
        self.total_deposits = 0
        self.total_withdrawals = 0

    def __repr__(self):
        return f"Bank(balance ={self.balance}, total_deposits = {self.total_deposits}, total_withdrawals = {self.total_withdrawals})"

    def process_order_type(self, order):
        if order.order_type == "buy":
            def withdrawals():
                pass
        elif order.order_type == "sell":
            def deposits():
                pass
        else:
            pass



bank1 = Bank(1000)
print(bank1)

