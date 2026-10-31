#Sepideh Soltaninejad

from tools.validation import  Validator

# ARMAN UPDATE 10/31/2026


class Order_Item:
    def __init__(self,
                 order_item_id,
                 customer_id,
                 customer_name,
                 product_id,
                 product_name,
                 price,
                 quantity,
                 ):

        self.order_item_id = order_item_id
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price


    @property
    def order_item_id(self):
        return self.__order_item_id

    @order_item_id.setter
    def order_item_id(self, order_item_id):
        Validator.order_item_id_validator(order_item_id)
        self.__order_item_id = order_item_id

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
    def quantity(self, quantity):
        Validator.quantity_validator(quantity)
        self.__quantity = quantity

    def __repr__(self):
        return (f"Orderitem({self.order_item_id}, {self.customer_id}, "
                f"{self.customer_name}, {self.product_id}, {self.product_name}, "
                f"{self.quantity}, {self.price})")

    def to_tuple(self):
        return (self.order_item_id,
                self.customer_id,
                self.customer_name,
                self.product_id,
                self.product_name,
                self.quantity,
                self.price)
