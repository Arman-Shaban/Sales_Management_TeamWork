# Tests for payments, banks and deliveries.
import unittest

from models.bank import Bank
from models.delivery import Delivery
from models.payment_transaction import OutgoingPayment, PaymentReceived, PaymentTransaction
from services.errors import BusinessRuleError, NotFoundError
from tests.base import StoreTestCase

CARD = "4111 1111 1111 1111"


class PaymentModelTest(unittest.TestCase):
    def test_receipt_numbers_grow(self):
        first, second = PaymentTransaction(10), OutgoingPayment(20)
        self.assertEqual(second.receipt_no, first.receipt_no + 1)

    def test_payment_received_keeps_card_and_payer(self):
        payment = PaymentReceived(50, "1111", payer="someone")
        self.assertEqual((payment.card_number, payment.payer, payment.total_amount),
                         ("1111", "someone", 50))

    def test_bank_and_delivery_models(self):
        self.assertEqual(Bank(1, "Nordea", "001").to_tuple(), (1, "Nordea", "001"))
        self.assertEqual(Delivery(1, 2, "Street 1", "pending").to_tuple()[3], "pending")
        with self.assertRaises(ValueError):
            Delivery(1, 2, "Street 1", "lost")
        with self.assertRaises(ValueError):
            Delivery(1, 2, "", "pending")


class PaymentServiceTest(StoreTestCase):
    def setUp(self):
        super().setUp()
        self.customer = self.make_customer()
        self.product = self.make_product(price=5, stock=10)

    def completed_order(self, order_type="sell", quantity=2):
        order = self.orders.create_order(self.customer.customer_id, order_type)
        self.orders.add_item(order.order_id, self.product.product_id, quantity)
        return self.orders.complete_order(order.order_id)

    def test_pay_sell_order(self):
        order = self.completed_order()
        payment = self.payments.pay_order(order.order_id, CARD)
        self.assertEqual(payment.total_amount, 10)
        self.assertEqual(payment.card_number, "1111")            # only the last 4 digits
        self.assertEqual(self.orders.get_order(order.order_id).payment_id, payment.receipt_no)
        self.assertEqual(len(self.payments.list_payments()), 1)

    def test_pay_buy_order_is_outgoing(self):
        order = self.completed_order("buy")
        payment = self.payments.pay_order(order.order_id)
        self.assertIsInstance(payment, OutgoingPayment)
        self.assertEqual(self.payments.get_payment(payment.receipt_no).kind, "OUTGOING")

    def test_payment_rules(self):
        pending = self.orders.create_order(self.customer.customer_id)
        with self.assertRaises(BusinessRuleError):
            self.payments.pay_order(pending.order_id, CARD)       # not completed
        order = self.completed_order()
        with self.assertRaises(ValueError):
            self.payments.pay_order(order.order_id, "12")         # bad card
        self.payments.pay_order(order.order_id, CARD)
        with self.assertRaises(BusinessRuleError):
            self.payments.pay_order(order.order_id, CARD)         # paid twice
        with self.assertRaises(NotFoundError):
            self.payments.pay_order(99, CARD)

    def test_paid_order_cannot_be_cancelled(self):
        order = self.completed_order()
        self.payments.pay_order(order.order_id, CARD)
        with self.assertRaises(BusinessRuleError):
            self.orders.cancel_order(order.order_id)

    def test_banks(self):
        bank = self.payments.add_bank("Nordea", "001")
        self.assertEqual([b.bank_name for b in self.payments.list_banks()], ["Nordea"])
        with self.assertRaises(BusinessRuleError):
            self.payments.add_bank("Nordea", "002")
        order = self.completed_order()
        self.payments.pay_order(order.order_id, CARD, bank.bank_id)
        with self.assertRaises(NotFoundError):
            self.payments.pay_order(self.completed_order().order_id, CARD, bank_id=99)


class DeliveryServiceTest(StoreTestCase):
    def setUp(self):
        super().setUp()
        customer = self.make_customer()
        product = self.make_product(price=5, stock=10)
        order = self.orders.create_order(customer.customer_id, "sell")
        self.orders.add_item(order.order_id, product.product_id, 1)
        self.order = self.orders.complete_order(order.order_id)

    def test_full_delivery_flow(self):
        delivery = self.deliveries.create_delivery(self.order.order_id, "Street 1")
        self.assertEqual(delivery.status, "pending")
        self.payments.pay_order(self.order.order_id, CARD)
        self.assertEqual(self.deliveries.ship(delivery.delivery_id).status, "shipped")
        done = self.deliveries.deliver(delivery.delivery_id)
        self.assertEqual(done.status, "delivered")
        self.assertNotEqual(done.delivered_at, "")

    def test_cannot_ship_before_payment(self):
        delivery = self.deliveries.create_delivery(self.order.order_id, "Street 1")
        with self.assertRaises(BusinessRuleError):
            self.deliveries.ship(delivery.delivery_id)

    def test_wrong_order_of_steps(self):
        delivery = self.deliveries.create_delivery(self.order.order_id, "Street 1")
        with self.assertRaises(BusinessRuleError):
            self.deliveries.deliver(delivery.delivery_id)          # not shipped yet
        self.deliveries.cancel(delivery.delivery_id)
        with self.assertRaises(BusinessRuleError):
            self.deliveries.cancel(delivery.delivery_id)

    def test_one_delivery_per_order_and_only_completed_sales(self):
        self.deliveries.create_delivery(self.order.order_id, "Street 1")
        with self.assertRaises(BusinessRuleError):
            self.deliveries.create_delivery(self.order.order_id, "Street 2")
        pending = self.orders.create_order(self.order.customer_id)
        with self.assertRaises(BusinessRuleError):
            self.deliveries.create_delivery(pending.order_id, "Street 3")


if __name__ == "__main__":
    unittest.main()
