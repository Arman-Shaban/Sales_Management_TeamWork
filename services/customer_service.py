# Business rules for customers.
import sqlite3

from models.customer import Customer
from repositories.customer_repositories import CustomerRepository
from services.errors import BusinessRuleError, NotFoundError
from tools.validation import Validator


class CustomerService:
    def __init__(self, db):
        self.db = db
        self.repo = CustomerRepository()

    def _check(self, customer):
        Validator.person_name_validator(customer.customer_name, "Name")
        Validator.person_name_validator(customer.customer_family, "Family")
        Validator.phone_validator(customer.customer_phone)

    def add(self, name, family, phone):
        customer = Customer(name.strip(), family.strip(), phone.strip())
        self._check(customer)
        try:
            with self.db.transaction() as conn:
                customer.customer_id = self.repo.insert(conn, customer)
        except sqlite3.IntegrityError:
            raise BusinessRuleError("A customer with this phone number already exists")
        return customer

    def update(self, customer_id, name, family, phone):
        with self.db.transaction() as conn:
            customer = self.repo.find_by_id(conn, customer_id)
            if customer is None:
                raise NotFoundError(f"Customer {customer_id} was not found")
            customer.customer_name = name.strip()
            customer.customer_family = family.strip()
            customer.customer_phone = phone.strip()
            self._check(customer)
            try:
                self.repo.update(conn, customer)
            except sqlite3.IntegrityError:
                raise BusinessRuleError("A customer with this phone number already exists")
        return customer

    def delete(self, customer_id):
        try:
            with self.db.transaction() as conn:
                if self.repo.find_by_id(conn, customer_id) is None:
                    raise NotFoundError(f"Customer {customer_id} was not found")
                self.repo.delete(conn, customer_id)
        except sqlite3.IntegrityError:
            raise BusinessRuleError("This customer has orders and cannot be deleted")

    def get(self, customer_id):
        with self.db.connection() as conn:
            customer = self.repo.find_by_id(conn, customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} was not found")
        return customer

    def list_all(self):
        with self.db.connection() as conn:
            return self.repo.find_all(conn)
