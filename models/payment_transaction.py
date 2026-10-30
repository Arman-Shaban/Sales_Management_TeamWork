#Nastaran
# می خوام بعدا لیست اقلام رو جدول مانند نشون بده

from datetime import datetime


class PaymentTransaction:
    next_no = 1001
    def __init__(self, total_amount):
        self.receipt_no = PaymentTransaction.next_no
        PaymentTransaction.next_no += 1
        self.total_amount = total_amount
        dt = datetime.now()
        self.date = dt.date()
        self.time = dt.time()

receipt1 = PaymentTransaction(1000)
print(receipt1.date.strftime("%d/%m/%y"))
print(receipt1.time.strftime("%H:%M:%S"))


class PaymentReceived(PaymentTransaction):
    def __init__(self, total_amount, payer, card_number ):
        super().__init__(total_amount)
        self.payer = payer
        self.card_number = card_number

class OutgoingPayment(PaymentTransaction):
    def __init__(self, total_amount):
        super().__init__(total_amount)
