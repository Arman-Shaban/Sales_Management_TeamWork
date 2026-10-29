#Sepideh

from model import *

from test import orderitem_test
from datetime import date, time, timedelta
from tools.validation import  Validator

#purchase_invoice: buy
#sales_invoice: sell
#basket_invoice: cart

class Order:
    def __init__(self, buy, sell, cart):
        self.order_id = order_id
        self.order_type = order_type
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.status = status
        self.total_price = total_price
        self.quantity = quantity
        self.payment_id = payment_id
        self.inventory_transaction_id = inventory_transaction_id
        self.date_time = date_time
        self.order_time = date.today() + timedelta(minutes=55)
        #self.buy_order = date.today() + timedelta(minutes=50)
        #self.sell_order = date.today() + timedelta(minutes=50)
        #self.cart = date.today() + timedelta(hours=24)

    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, order_id):
        Validator.order_id_validator(order_id)
        self.__order_id = order_id

    @property
    def order_type(self):
        return self.__order_type

    @order_name.setter
    def order_type(self, order_type):
        Validator.order_type_validator(order_type)
        self.__order_type = order_type

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def customer_id(self, customer_id):
        Validator.customer_id_validator(customer_id)
        self.__customer_id = customer_id

    @property
    def customer_name(self):
        return self.__customer_name

    @customer_name.setter
    def customer_name(self, customer_name):
        Validator.customer_name_validator(customer_name)
        self.__customer_name = customer_name

    @property
    def statuse(self):
        return self.__statuse

    @statuse.setter
    def statuse(self, statuse):
        Validator.statuse_validator(statuse)
        self.__statuse = statuse

    @property
    def total_price(self):
        return self.__total_price

    @total_price.setter
    def total_price(self, total_price):
        Validator.total_price_validator(total_price)
        self.__total_price = total_price

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, quantity):
        Validator.quantity_validator(quantity)
        self.__quantity = quantity

    @property
    def payment_id(self):
        return self.__payment_id

    @payment_id.setter
    def payment_id(self, payment_id):
        Validator.payment_id_validator(payment_id)
        self.__payment_id = payment_id

     @property
    def inventory_transaction_id(self):
        return self.__inventory_transaction_id

    @customer_id.setter
    def inventory_transaction_id(self, inventory_transaction_id):
        Validator.inventory_transaction_id_validator(inventory_transaction_id)
        self.__inventory_transaction_id = inventory_transaction_id

    @property
    def date_time(self):
        return self.__date_time

    @date_time.setter
    def date_time(self, date_time):
        Validator.date_time_validator(date_time)
        self.__date_time = date_time

    @property
    def order_time(self):
        return self.__order_time

    @order_time.setter
    def order_time(self, order_time):
        Validator.order_time_validator(order_time)
        self.__order_time = order_time

    def __repr__(self):
        return (f"Order"
        ({self.order_id},
         {self.order_type},
         {self.customer_id},
         {self.customer_name},
         {self.statuse},
         {self.total_price},
         {self.payment_id},
         {self.inventory_transaction_id},
         {self.quantity},
         {self.date_time},
         {self.order_time}))

    def to_tuple(self):
        return (self.order_id,
                self.order_type,
                self.customer_id,
                self.customer_name,
                self.statuse,
                self.total_price,
                self.payment_id,
                self.inventory_transaction_id,
                self.quantity,
                self.date_time)
