import time

class Delivery:
    def __init__(self, delivery_address, delivery_postal_code):
        self.address = delivery_address
        self.postal_code = delivery_postal_code
        self.deliver_status = "pending"

    def __repr__(self):
        return f"Delivery( address = {self.address}, postal code = {self.postal_code}, delivery status = {self.deliver_status})"

    def start_preparing(self):
        self.deliver_status = "Preparing"

    def shipping(self):
        self.deliver_status = "Shipped"

    def delivery(self):
        self.deliver_status = "Delivered"

    def show_delivery_status(self):
        print(f" Your Delivery Status: {self.deliver_status}")


address = input(" Enter Your Address :")
postal_code = int(input("Enter Your postal code : "))
delivery1 = Delivery(address, postal_code)
delivery1.show_delivery_status()
# print(delivery1)
time.sleep(5)
delivery1.start_preparing()
delivery1.show_delivery_status()
# print(delivery1)
time.sleep(10)
delivery1.shipping()
delivery1.show_delivery_status()
# print(delivery1)
time.sleep(15)
delivery1.delivery()
delivery1.show_delivery_status()
# print(delivery1)


