#Nastaran
# نمی تونم مشتری رو از ماژول مشتری فراخوانی کنمnastaran
# (The total price now comes from the order: PaymentService passes order.total_price.)

from datetime import datetime
from models.customer import Customer
from persian_tools.bank import card_number

# ARMAN UPDATE 10/31/2026


class PaymentTransaction:
    next_no = 1001
    def __init__(self, total_amount):
        self.receipt_no = PaymentTransaction.next_no
        PaymentTransaction.next_no += 1
        self.total_amount = total_amount
        dt = datetime.now()
        self.date = dt.date()
        self.time = dt.time().replace(microsecond=0)

    def __repr__(self):
       return f"PaymentTransaction(number= {self.receipt_no}, total_amount = {self.total_amount})"


class PaymentReceived(PaymentTransaction):
    def __init__(self, total_amount, payer, card_number):
        super().__init__(total_amount)
        self.payer = payer         # a Customer object (it was the Customer class itself before)
        self.card_number = card_number

    def __repr__(self):
        return f"PaymentReceived(payer = {self.payer})"

    @staticmethod
    def get_card_number():
        card_number = input("Please Enter Your Card Number: ")
        return card_number

    def validate_card_number(self):
        card_number.validate(self.card_number)




class OutgoingPayment(PaymentTransaction):
    def __init__(self, total_amount):
        super().__init__(total_amount)


# Console demo (only when this file is run directly, not on import)
if __name__ == "__main__":
    receipt1 = PaymentTransaction(1000)
    print(receipt1.date.strftime("%d/%m/%y"))
    print(receipt1.time.strftime("%H:%M:%S"))
    print(receipt1)
    payment_receipt = PaymentReceived(1000, "customer1", 56)
    print(payment_receipt)
    payment_receipt.get_card_number()
    payment_receipt.validate_card_number()