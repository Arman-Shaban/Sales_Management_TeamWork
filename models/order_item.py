#Sepideh

from test import orderitem_test
from datetime import date, timedelta, time
from tools.validation import  Validator


class Order_item:
    def __init__(self, order_item_id, customer_name, product_id , price, quantity, date, time):
        self.order_item_id = order_item_id
        self.customer_name = customer_name
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price
        #self.orderitem_time = time
        #self.orderitem_date = date.today()

    @property
    def order_item_id(self):
        return self.__order_item_id

    @order_item_id.setter
    def order_item_id(self, order_item_id):
        Validator.order_item_id_validator(order_item_id)
        self.__order_item_id = order_item_id

    @property
    def customer_name(self):
        return self.__customer_name

    @customer_name.setter
    def customer_name(self, customer_name):
        Validator.customer_name_validator(customer_name)
        self.__customer_name = customer_name

    @property
    def product_id(self):
        return self.__product_id

    @product_id.setter
    def product_id(self, product_id):
        Validator.product_id_validator(product_id)
        self.__product_id = product_id

    @property
    def product_name(self):
        return self.__product_name

    @product_name.setter
    def product_name(self, product_name):
        Validator.product_name_validator(product_name)
        self.__product_name = product_name

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        Validator.price_validator(price)
        self.__price = price

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def price(self, quantity):
        Validator.quantity_validator(quantity)
        self.__quantity = quantity

    def __repr__(self):
        return (f"Orderitem "
        ({self.order_item_id},
         {self.customer_name},
         {self.product_id},
         {self.product_name},
         {self.quantity},{self.price}))

    def to_tuple(self):
        return (self.order_item_id,
                self.customer_name,
                self.product_id,
                self.product_name,
                self.quantity,
                self.price)
