# Tests for products, inventory and inventory transactions.
import unittest

from models.inventory import Inventory
from models.inventory_transaction import Inventory_Transaction
from models.product import Product
from services.errors import BusinessRuleError, NotFoundError
from tests.base import StoreTestCase


class InventoryModelTest(unittest.TestCase):
    def test_inventory_rejects_negative_quantity(self):
        with self.assertRaises(ValueError):
            Inventory(1, 1, -5, 2)

    def test_deficient_amount_property_works(self):
        inventory = Inventory(1, 1, 10, 3)
        inventory.deficient_amount = 4
        self.assertEqual(inventory.deficient_amount, 4)
        self.assertEqual(inventory.to_tuple(), (1, 10, 1, 4))

    def test_transaction_rejects_unknown_type(self):
        with self.assertRaises(ValueError):
            Inventory_Transaction(1, "STEAL", "2026-01-01 10:00:00", 1, 2, 0)

    def test_transaction_rejects_bad_date(self):
        with self.assertRaises(ValueError):
            Inventory_Transaction(1, "SALE", "yesterday", 1, 2, 0)

    def test_product_needs_valid_values(self):
        self.assertEqual(Product(1, "Pen", "Bic", 5, 2.5).to_tuple(), (1, "Pen", "Bic", 5, 2.5))
        with self.assertRaises(ValueError):
            Product(1, "Pen", "Bic", 5, 0)        # price must be positive


class InventoryServiceTest(StoreTestCase):
    def test_new_product_gets_inventory_and_first_transaction(self):
        product = self.make_product(stock=10)
        self.assertEqual(self.stock_of(product.product_id), 10)
        transactions = self.inventory.list_transactions(product.product_id)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].inventory_transaction_type, "ADDITION")

    def test_addition_and_sale_change_stock(self):
        product = self.make_product(stock=10)
        self.inventory.add_transaction("ADDITION", product.product_id, 5)
        self.inventory.add_transaction("SALE", product.product_id, 3)
        self.assertEqual(self.stock_of(product.product_id), 12)

    def test_cannot_sell_more_than_stock(self):
        product = self.make_product(stock=2)
        with self.assertRaises(BusinessRuleError):
            self.inventory.add_transaction("SALE", product.product_id, 3)
        self.assertEqual(self.stock_of(product.product_id), 2)      # nothing changed

    def test_unknown_product_or_order(self):
        with self.assertRaises(NotFoundError):
            self.inventory.add_transaction("ADDITION", 99, 1)
        product = self.make_product()
        with self.assertRaises(NotFoundError):
            self.inventory.add_transaction("ADDITION", product.product_id, 1, order_id=99)

    def test_low_stock_list(self):
        low = self.make_product("Low", stock=3)        # default limit is 5
        self.make_product("Fine", stock=50)
        result = self.inventory.list_low_stock()
        self.assertEqual([i.product_id for i in result], [low.product_id])

    def test_update_deficient_amount(self):
        product = self.make_product(stock=10)
        inventory = self.inventory.get_by_product(product.product_id)
        self.inventory.update_deficient_amount(inventory.inventory_id, 20)
        self.assertEqual(len(self.inventory.list_low_stock()), 1)

    def test_product_update_and_delete(self):
        product = self.make_product()
        self.products.update(product.product_id, "Pencil", "Faber", 1.5)
        self.assertEqual(self.products.get(product.product_id).product_name, "Pencil")
        self.products.delete(product.product_id)
        with self.assertRaises(NotFoundError):
            self.products.get(product.product_id)

    def test_product_used_in_order_cannot_be_deleted(self):
        customer, product = self.make_customer(), self.make_product()
        order = self.orders.create_order(customer.customer_id)
        self.orders.add_item(order.order_id, product.product_id, 1)
        with self.assertRaises(BusinessRuleError):
            self.products.delete(product.product_id)


if __name__ == "__main__":
    unittest.main()
