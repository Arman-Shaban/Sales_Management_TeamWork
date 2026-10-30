#Nastaran
# می خوام بعدا لیست اقلام رو جدول مانند نشون بده
#  نمیتونم از order ایمپورت کنم قیمت کل رو نشون بده سر همین متود total_amount مونده

from datetime import datetime
from customer import name

class PaymentTransaction:
    next_no = 1001
    def __init__(self, total_amount):
        self.receipt_no = PaymentTransaction.next_no
        PaymentTransaction.next_no += 1
        self.total_amount = total_amount
        dt = datetime.now()
        self.date = dt.date()
        self.time = dt.time().replace(microsecond=0)

    @staticmethod
    def total_amount():
        pass

    def __repr__(self):
       return f"PaymentTransaction(number= {self.receipt_no},date = {self.date}, time = {self.time}, total_amount = {self.total_amount})"

receipt1 = PaymentTransaction(1000)
print(receipt1)
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
