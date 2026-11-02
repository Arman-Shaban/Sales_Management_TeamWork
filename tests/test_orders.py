# Tests for customers and orders.
import unittest

from models.order import Order
from services.errors import BusinessRuleError, NotFoundError
from tests.base import StoreTestCase


class OrderModelTest(unittest.TestCase):
    def make_order(self, **changes):
        values = dict(order_id=1, order_type="sell", customer_id=1, customer_name="Ali",
                      status="pending", total_price=10, quantity=2, payment_id=0,
                      inventory_transaction_id=0, date_time="2026-10-31 10:00:00")
        values.update(changes)
        return Order(**values)

    def test_valid_order(self):
        order = self.make_order()
        self.assertEqual(order.order_id, 1)
        self.assertEqual(order.total_price, 10)
        self.assertEqual(len(order.to_tuple()), 11)

    def test_order_time_is_set_automatically(self):
        self.assertTrue(self.make_order().order_time)

    def test_bad_values_are_rejected(self):
        for bad in ({"order_type": "gift"}, {"status": "lost"}, {"total_price": -1},
                    {"quantity": -2}, {"customer_name": ""}, {"date_time": "today"}):
            with self.assertRaises(ValueError):
                self.make_order(**bad)


class CustomerServiceTest(StoreTestCase):
    def test_add_and_list(self):
        customer = self.make_customer()
        self.assertEqual(customer.customer_id, 1)
        self.assertEqual(len(self.customers.list_all()), 1)

    def test_phone_must_be_unique(self):
        self.make_customer("0401234567")
        with self.assertRaises(BusinessRuleError):
            self.make_customer("0401234567")

    def test_invalid_data(self):
        with self.assertRaises(ValueError):
            self.customers.add("", "Rezai", "0401234567")
        with self.assertRaises(ValueError):
            self.customers.add("Ali", "Rezai", "abc")

    def test_update_and_delete(self):
        customer = self.make_customer()
        self.customers.update(customer.customer_id, "Reza", "Ahmadi", "0509999999")
        self.assertEqual(self.customers.get(customer.customer_id).customer_name, "Reza")
        self.customers.delete(customer.customer_id)
        with self.assertRaises(NotFoundError):
            self.customers.get(customer.customer_id)


class OrderServiceTest(StoreTestCase):
    def setUp(self):
        super().setUp()
        self.customer = self.make_customer()
        self.product = self.make_product(price=2.5, stock=10)

    def new_order(self, order_type="sell"):
        return self.orders.create_order(self.customer.customer_id, order_type)

    def test_create_order(self):
        order = self.new_order()
        self.assertEqual(order.status, "pending")
        self.assertEqual(order.customer_name, "Ali Rezai")
        with self.assertRaises(NotFoundError):
            self.orders.create_order(99)

    def test_totals_follow_the_items(self):
        order = self.new_order()
        order = self.orders.add_item(order.order_id, self.product.product_id, 3)
        self.assertEqual(order.quantity, 3)
        self.assertEqual(order.total_price, 7.5)

    def test_complete_sell_order_reduces_stock(self):
        order = self.new_order()
        self.orders.add_item(order.order_id, self.product.product_id, 4)
        done = self.orders.complete_order(order.order_id)
        self.assertEqual(done.status, "completed")
        self.assertNotEqual(done.inventory_transaction_id, 0)
        self.assertEqual(self.stock_of(self.product.product_id), 6)

    def test_complete_buy_order_increases_stock(self):
        order = self.new_order("buy")
        self.orders.add_item(order.order_id, self.product.product_id, 5)
        self.orders.complete_order(order.order_id)
        self.assertEqual(self.stock_of(self.product.product_id), 15)

    def test_cart_becomes_sell_when_completed(self):
        order = self.new_order("cart")
        self.orders.add_item(order.order_id, self.product.product_id, 1)
        self.assertEqual(self.orders.complete_order(order.order_id).order_type, "sell")

    def test_cannot_complete_empty_order(self):
        with self.assertRaises(BusinessRuleError):
            self.orders.complete_order(self.new_order().order_id)

    def test_cancel_completed_sell_order_gives_stock_back(self):
        order = self.new_order()
        self.orders.add_item(order.order_id, self.product.product_id, 4)
        self.orders.complete_order(order.order_id)
        self.orders.cancel_order(order.order_id)
        self.assertEqual(self.stock_of(self.product.product_id), 10)
        self.assertEqual(self.orders.get_order(order.order_id).status, "cancelled")

    def test_cancel_pending_order(self):
        order = self.new_order()
        self.assertEqual(self.orders.cancel_order(order.order_id).status, "cancelled")
        with self.assertRaises(BusinessRuleError):
            self.orders.cancel_order(order.order_id)           # already cancelled

    def test_completed_order_cannot_be_changed(self):
        order = self.new_order()
        self.orders.add_item(order.order_id, self.product.product_id, 1)
        self.orders.complete_order(order.order_id)
        with self.assertRaises(BusinessRuleError):
            self.orders.add_item(order.order_id, self.product.product_id, 1)
        with self.assertRaises(BusinessRuleError):
            self.orders.complete_order(order.order_id)

    def test_delete_pending_order_removes_items(self):
        order = self.new_order()
        self.orders.add_item(order.order_id, self.product.product_id, 1)
        self.orders.delete_order(order.order_id)
        self.assertEqual(self.orders.list_orders(), [])


if __name__ == "__main__":
    unittest.main()
