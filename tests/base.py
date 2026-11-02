# Shared test helper: every test gets its own empty temporary database.
import os
import shutil
import tempfile
import unittest

from database.connection import Database
from database.init_db import initialize
from services.customer_service import CustomerService
from services.delivery_service import DeliveryService
from services.inventory_service import InventoryService
from services.order_service import OrderService
from services.payment_service import PaymentService
from services.product_service import ProductService


class StoreTestCase(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.db = Database(os.path.join(self.folder, "test.db"))
        initialize(self.db)
        self.customers = CustomerService(self.db)
        self.products = ProductService(self.db)
        self.inventory = InventoryService(self.db)
        self.orders = OrderService(self.db)
        self.payments = PaymentService(self.db)
        self.deliveries = DeliveryService(self.db)

    def tearDown(self):
        shutil.rmtree(self.folder, ignore_errors=True)

    # quick ways to create test data
    def make_customer(self, phone="0401234567"):
        return self.customers.add("Ali", "Rezai", phone)

    def make_product(self, name="Pen", price=2.5, stock=10):
        return self.products.add(name, "Bic", price, stock)

    def stock_of(self, product_id):
        return self.products.get(product_id).stock_inventory
