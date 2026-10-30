#Sepideh Soltaninejad updated

from datetime import date, timedelta, time
from tools.validation import Validator
from models import *


class Inventory_Transaction:
    def __init__(self, 
                 inventory_transaction_id,
                 inventory_transaction_type,
                 inventory_transaction_datetime,
                 product_id,
                 quantity,
                 order_id):

        self.inventory_transaction_id = inventory_transaction_id
        self.inventory_transaction_type = inventory_transaction_type
        self.inventory_transaction_datetime = inventory_transaction_datetime
        self.product_id = product_id
        self.quantity = quantity
        self.order_id = order_id

    @property
    def inventory_transaction_id(self):
        return self.__inventory_transaction_id

    @inventory_transaction_id.setter
    def inventory_transaction_id(self, inventory_transaction_id):
        Validator.inventory_transaction_id(inventory_transaction_id)
        self.__inventory_transaction_id = inventory_transaction_id

    @property
    def inventory_transaction_type(self):
        return self.__inventory_transaction_type

    @inventory_transaction_type.setter
    def inventory_transaction_type(self, inventory_transaction_type):
        Validator.inventory_transaction_type(inventory_transaction_type)
        self.__inventory_transaction_type = inventory_transaction_type

    @property
    def inventory_transaction_datetime(self):
        return self.__inventory_transaction_datetime

    @inventory_transaction_datetime.setter
    def inventory_transaction_datetime(self, inventory_transaction_datetime):
        Validator.inventory_transaction_datetime(inventory_transaction_datetime)
        self.__inventory_transaction_datetime = inventory_transaction_datetime

    @order_id
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, order_id):
        Validator.order_id(order_id)
        self.__order_id = order_id

    @product_id
    def product_id(self):
        return self.__product_id

    @product_id.setter
    def product_id(self, product_id):
        Validator.product_id(product_id)
        self.__product_id = product_id

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity):
        Validator.quantity(quantity)
        self.__quantity = quantity


    def __repr__(self):
        return (f"Inventory_Transaction"
        ({self.inventory_transaction_id},
        {self.inventory_transaction_type},
        {self.inventory_transaction_datetime},
        {self.product_id},
        {self.quantity},
        {self.order_id}))

    def to_tuple(self):
        return (self.inventory_transaction_id,
                self.inventory_transaction_type,
                self.inventory_transaction_datetime,
                self.quantity,
                self.product_id,
                self.order_id)

