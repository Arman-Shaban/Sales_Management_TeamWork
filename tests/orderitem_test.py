# Tests for order items (model and the add/remove rules of the order service).
import unittest

from models.order_item import Order_Item
from services.errors import BusinessRuleError, NotFoundError
from tests.base import StoreTestCase


class OrderItemModelTest(unittest.TestCase):
    def test_valid_item(self):
        item = Order_Item(1, 1, "Ali", 2, "Pen", 2.5, 3)
        self.assertEqual(item.to_tuple(), (1, 1, "Ali", 2, "Pen", 3, 2.5))

    def test_price_and_quantity_are_separate(self):
        # the quantity setter was once named "price" by mistake
        item = Order_Item(1, 1, "Ali", 2, "Pen", 2.5, 3)
        item.quantity = 7
        self.assertEqual(item.price, 2.5)
        self.assertEqual(item.quantity, 7)

    def test_bad_values_are_rejected(self):
        with self.assertRaises(ValueError):
            Order_Item(1, 1, "Ali", 2, "Pen", 2.5, 0)        # quantity must be at least 1
        with self.assertRaises(ValueError):
            Order_Item(1, 1, "Ali", 2, "Pen", -1, 1)         # negative price
        with self.assertRaises(ValueError):
            Order_Item(1, 1, "", 2, "Pen", 2.5, 1)           # empty customer name


class OrderItemServiceTest(StoreTestCase):
    def setUp(self):
        super().setUp()
        customer = self.make_customer()
        self.pen = self.make_product("Pen", 2.5, stock=10)
        self.book = self.make_product("Book", 10, stock=2)
        self.order = self.orders.create_order(customer.customer_id, "sell")

    def test_same_product_twice_adds_the_quantity(self):
        self.orders.add_item(self.order.order_id, self.pen.product_id, 2)
        self.orders.add_item(self.order.order_id, self.pen.product_id, 3)
        items = self.orders.list_items(self.order.order_id)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].quantity, 5)

    def test_item_keeps_price_and_names(self):
        self.orders.add_item(self.order.order_id, self.pen.product_id, 1)
        item = self.orders.list_items(self.order.order_id)[0]
        self.assertEqual((item.product_name, item.price, item.customer_name),
                         ("Pen", 2.5, "Ali Rezai"))

    def test_not_enough_stock(self):
        with self.assertRaises(BusinessRuleError):
            self.orders.add_item(self.order.order_id, self.book.product_id, 3)
        self.orders.add_item(self.order.order_id, self.book.product_id, 2)
        with self.assertRaises(BusinessRuleError):           # 2 + 1 is more than the stock
            self.orders.add_item(self.order.order_id, self.book.product_id, 1)

    def test_remove_item_updates_total(self):
        self.orders.add_item(self.order.order_id, self.pen.product_id, 2)
        self.orders.add_item(self.order.order_id, self.book.product_id, 1)
        item = self.orders.list_items(self.order.order_id)[0]
        order = self.orders.remove_item(item.order_item_id)
        self.assertEqual(order.total_price, 10)
        self.assertEqual(order.quantity, 1)

    def test_unknown_ids(self):
        with self.assertRaises(NotFoundError):
            self.orders.add_item(self.order.order_id, 99, 1)
        with self.assertRaises(NotFoundError):
            self.orders.remove_item(99)
        with self.assertRaises(NotFoundError):
            self.orders.list_items(99)

    def test_bad_quantity(self):
        with self.assertRaises(ValueError):
            self.orders.add_item(self.order.order_id, self.pen.product_id, 0)


if __name__ == "__main__":
    unittest.main()
