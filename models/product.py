#Sepideh
from tools.validation import Validator

class Product:
    def __init__(self, product_id, product_name, stock_inventory, price):
        self.product_id = product_id
        self.product_name = product_name
        self.product_brand = product_brand
        self.stock_inventory = stock_inventory     #quantity
        self.price = price

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
    def product_name(self):
        return self.__product_name

    @product_brand.setter
    def product_brand(self, product_brand):
        Validator.product_brand_validator(product_brand)
        self.__product_brand = product_brand
        
    @property
    def stock_inventory(self):
        return self.__stock_inventory

    @stock_inventory.setter
    def stock_inventory(self, stock_inventory):
        Validator.stock_inventory_validator(stock_inventory)
        self.__stock_inventory = stock_inventory

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        Validator.price_validator(price)
        self.__price = price

    def __repr__(self):
        return (f"Product "
        ({self.product_id},
         {self.product_name},
         {self.product_brand},
         {self.stock_inventory},
         {self.price}))

    def to_tuple(self):
        return (self.product_id,
                self.product_name,
                self.product_brand,
                self.stock_inventory,
                self.price)
