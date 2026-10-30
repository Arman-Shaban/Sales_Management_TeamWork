#Nastaran
# می خوام بعدا لیست اقلام رو جدول مانند نشون بده
#  نمیتونم از order ایمپورت کنم قیمت کل رو نشون بده سر همین متود total_amount مونده

from datetime import datetime
from customer import Customer

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
       return f"PaymentTransaction(number= {self.receipt_no}, total_amount = {self.total_amount})"

receipt1 = PaymentTransaction(1000)
print(receipt1.date.strftime("%d/%m/%y"))
print(receipt1.time.strftime("%H:%M:%S"))
print(receipt1)

class PaymentReceived(PaymentTransaction):
    def __init__(self, total_amount, card_number ):
        super().__init__(total_amount)
        self.payer = Customer
        self.card_number = card_number

    @staticmethod
    def get_card_number():
        card_number = input("Please Enter Your Card Number: ")



receipt2 = PaymentReceived



class OutgoingPayment(PaymentTransaction):
    def __init__(self, total_amount):
        super().__init__(total_amount)
