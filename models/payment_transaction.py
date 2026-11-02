#Nastaran
# (The total price now comes from the order: PaymentService passes order.total_price.)

from datetime import datetime
from irvalidate import is_valid_card_number, validate_card_number

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

    @staticmethod
    def get_card_number():
        attempt = 0
        while attempt < 3:
            card_number = input("Please Enter Your Card Number: ")
            if validate_card_number(card_number):
                return card_number
            else:
                attempt += 1
                remaining_attempts = 3 - attempt
                print(f"Error: Invalid Card Number! remaining attempts = {remaining_attempts}")
        print("Error: Maximum Attempts Reached!")
        return None


    @staticmethod
    def validate_card_number(card_number):
        return is_valid_card_number(card_number)


# Console demo (only when this file is run directly, not on import)
if __name__ == "__main__":
    receipt1 = PaymentTransaction(1000)
    print(receipt1.date.strftime("%d/%m/%y"))
    print(receipt1.time.strftime("%H:%M:%S"))
    print(receipt1)
    card = receipt1.get_card_number()
    receipt1.validate_card_number(card)
