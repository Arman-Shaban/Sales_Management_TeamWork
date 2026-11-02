from payment_transaction import PaymentTransaction

class PaymentReceived(PaymentTransaction):
    def __init__(self, total_amount, payer, card_number):
        super().__init__(total_amount)
        self.payer = payer         # a Customer object (it was the Customer class itself before)
        self.card_number = card_number


 def __repr__(self):
        return f"PaymentReceived(payer = {self.payer})"


class OutgoingPayment(PaymentTransaction):
    def __init__(self, total_amount):
        super().__init__(total_amount)


    payment_receipt = PaymentReceived(1000, "customer1", 56)
    print(payment_receipt)
    payment_receipt.get_card_number()
    payment_receipt.validate_card_number()