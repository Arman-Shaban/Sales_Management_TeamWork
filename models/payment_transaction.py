#Nastaran
# می خوام بعدا لیست اقلام رو جدول مانند نشون بده
from datetime import datetime
class PaymentTransaction:
    def __init__(self, receipt_no, total_amount, date = None, time = None):
        self.receipt_no = receipt_no
        self.total_amount = total_amount
        self.date = date
        self.time = time

    def payment_date(self):
        dt =datetime.now()
        return dt

receipt1 = PaymentTransaction(1, 1000)
print(receipt1.payment_date())


class PaymentReceived(PaymentTransaction):
    def __init__(self, payyer, card_number ):
        self.payyer = payyer
        self.card_number = card_number

class OutgoingPayment(PaymentTransaction):
    def __init__(self):
        pass
