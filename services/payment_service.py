# Business rules for banks and payments.
import sqlite3

from models.bank import Bank
from models.payment_transaction import PaymentReceived, OutgoingPayment
from repositories.customer_repositories import CustomerRepository
from repositories.order_repositories import OrderRepository
from repositories.payment_repositories import PaymentRepository
from services.errors import BusinessRuleError, NotFoundError
from tools.validation import Validator


class PaymentService:
    def __init__(self, db):
        self.db = db
        self.repo = PaymentRepository()
        self.order_repo = OrderRepository()
        self.customer_repo = CustomerRepository()

    # ----- banks -----
    def add_bank(self, name, branch_code):
        bank = Bank(0, name.strip(), branch_code.strip())
        try:
            with self.db.transaction() as conn:
                bank.bank_id = self.repo.insert_bank(conn, bank)
        except sqlite3.IntegrityError:
            raise BusinessRuleError("A bank with this name already exists")
        return bank

    def list_banks(self):
        with self.db.connection() as conn:
            return self.repo.find_all_banks(conn)

    # ----- payments -----
    def pay_order(self, order_id, card_number="", bank_id=None):
        """Pay a completed order. A sell order is paid by the customer (card needed),
        a buy order is paid to the supplier."""
        with self.db.transaction() as conn:
            order = self.order_repo.find_by_id(conn, order_id)
            if order is None:
                raise NotFoundError(f"Order {order_id} was not found")
            if order.status != "completed":
                raise BusinessRuleError("Only completed orders can be paid")
            if order.payment_id != 0:
                raise BusinessRuleError("This order is already paid")
            if bank_id is not None and self.repo.find_bank_by_id(conn, bank_id) is None:
                raise NotFoundError(f"Bank {bank_id} was not found")

            if order.order_type == "sell":
                Validator.card_number_validator(card_number)
                digits = card_number.replace(" ", "").replace("-", "")
                customer = self.customer_repo.find_by_id(conn, order.customer_id)
                payment = PaymentReceived(order.total_price, digits[-4:], customer)  # keep 4 digits only
                kind = "RECEIVED"
            else:
                payment = OutgoingPayment(order.total_price)
                kind = "OUTGOING"

            payment.receipt_no = self.repo.insert_payment(
                conn, payment, order_id, kind, order.customer_id, bank_id)
            payment.order_id = order_id
            payment.kind = kind

            order.payment_id = payment.receipt_no
            self.order_repo.update(conn, order)
        return payment

    def get_payment(self, payment_id):
        with self.db.connection() as conn:
            payment = self.repo.find_payment_by_id(conn, payment_id)
        if payment is None:
            raise NotFoundError(f"Payment {payment_id} was not found")
        return payment

    def list_payments(self):
        with self.db.connection() as conn:
            return self.repo.find_all_payments(conn)
