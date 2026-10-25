#person2

from datetime import date, timedelta, time
from tools.validation import Validator
from model import order


class  Inventory:
    def __init__(self, inventory_id,
                 product_id,
                 inventory_quantity,
                 deficit_amount,
                 inventory_time,
                 inventory_date):

        self.inventory_id = Inventory
        self.product_id = product_id
        self.inventory_quantity = inventory_quantity
        self.deficit_amount= deficit_amount
        self.inventory_time = time
        self.inventory_date = date.today()
        #self.entry_time = en_time
        #self.exit_time= ex_time

    @property
    def inventory_id(self):
        return self.__inventory_id

    @inventory_id.setter
    def inventory_id(self, inventory_id):
        Validator.inventory_id(inventory_id)
        self.__inventory_id = inventory_id

    @property
    def inventory_quantity(self):
        return self.__inventory_quantity

    @inventory_quantity.setter
    def inventory_quantity(self, inventory_quantity):
        Validator.inventory_quantity(inventory_quantity)
        self.__inventory_quantity = inventory_quantity

    @property
    def defecit_amount(self):
        return self.__deficit_amount

    @deficit_amount.setter
    def deficint_amount(self, deficit_amount):
        Validator.deficit_amount(deficit_amount)
        self.__deficit_amount = deficit_amount

    def __repr__(self):
        return (f"Inventory"
        ({self.inventory_id},
        {self.inventory_quantity},
        {self.product_id},
        {self.deficit_amount}))

    def to_tuple(self):
        return (self.inventory_id,
                self.inventory_quantity,
                self.product_id,
                self.deficit_amount)

