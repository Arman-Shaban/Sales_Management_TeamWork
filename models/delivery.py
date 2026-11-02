#person1
from tools.validation import Validator

# ARMAN UPDATE 11/2/2026


class Delivery:
    def __init__(self, delivery_id, order_id, address, status,
                 shipped_at="", delivered_at=""):
        self.delivery_id = delivery_id
        self.order_id = order_id
        self.address = address
        self.status = status                # pending, shipped, delivered, cancelled
        self.shipped_at = shipped_at        # empty text until the order is shipped
        self.delivered_at = delivered_at    # empty text until the order is delivered

    @property
    def delivery_id(self):
        return self.__delivery_id

    @delivery_id.setter
    def delivery_id(self, delivery_id):
        Validator.delivery_id_validator(delivery_id)
        self.__delivery_id = delivery_id

    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, order_id):
        Validator.order_id_validator(order_id)
        self.__order_id = order_id

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        Validator.address_validator(address)
        self.__address = address

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        Validator.delivery_status_validator(status)
        self.__status = status

    @property
    def shipped_at(self):
        return self.__shipped_at

    @shipped_at.setter
    def shipped_at(self, shipped_at):
        Validator.optional_date_validator(shipped_at)
        self.__shipped_at = shipped_at

    @property
    def delivered_at(self):
        return self.__delivered_at

    @delivered_at.setter
    def delivered_at(self, delivered_at):
        Validator.optional_date_validator(delivered_at)
        self.__delivered_at = delivered_at

    def __repr__(self):
        return (f"Delivery({self.delivery_id}, {self.order_id}, {self.address}, "
                f"{self.status}, {self.shipped_at}, {self.delivered_at})")

    def to_tuple(self):
        return (self.delivery_id,
                self.order_id,
                self.address,
                self.status,
                self.shipped_at,
                self.delivered_at)
