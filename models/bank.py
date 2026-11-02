#person1
from tools.validation import Validator

# ARMAN UPDATE 11/2/2026

class Bank:
    def __init__(self, bank_id, bank_name, branch_code):
        self.bank_id = bank_id
        self.bank_name = bank_name
        self.branch_code = branch_code

    @property
    def bank_id(self):
        return self.__bank_id

    @bank_id.setter
    def bank_id(self, bank_id):
        Validator.bank_id_validator(bank_id)
        self.__bank_id = bank_id

    @property
    def bank_name(self):
        return self.__bank_name

    @bank_name.setter
    def bank_name(self, bank_name):
        Validator.bank_name_validator(bank_name)
        self.__bank_name = bank_name

    @property
    def branch_code(self):
        return self.__branch_code

    @branch_code.setter
    def branch_code(self, branch_code):
        Validator.branch_code_validator(branch_code)
        self.__branch_code = branch_code

    def __repr__(self):
        return f"Bank({self.bank_id}, {self.bank_name}, {self.branch_code})"

    def to_tuple(self):
        return (self.bank_id,
                self.bank_name,
                self.branch_code)
