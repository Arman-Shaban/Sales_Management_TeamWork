# SQL for banks and payment transactions.
from datetime import date, time

from models.bank import Bank
from models.payment_transaction import PaymentReceived, OutgoingPayment


class PaymentRepository:

    # ----- banks -----
    def insert_bank(self, conn, bank):
        cursor = conn.execute("INSERT INTO banks (name, branch_code) VALUES (?, ?)",
                              (bank.bank_name, bank.branch_code))
        return cursor.lastrowid

    def find_all_banks(self, conn):
        rows = conn.execute("SELECT * FROM banks ORDER BY id").fetchall()
        return [Bank(row["id"], row["name"], row["branch_code"]) for row in rows]

    def find_bank_by_id(self, conn, bank_id):
        row = conn.execute("SELECT * FROM banks WHERE id = ?", (bank_id,)).fetchone()
        return Bank(row["id"], row["name"], row["branch_code"]) if row else None

    # ----- payments -----
    def _to_payment(self, row):
        if row["kind"] == "RECEIVED":
            payment = PaymentReceived(row["total_amount"], row["card_last4"])
        else:
            payment = OutgoingPayment(row["total_amount"])
        payment.receipt_no = row["id"]                        # id from the database
        payment.date = date.fromisoformat(row["pay_date"])
        payment.time = time.fromisoformat(row["pay_time"])
        # The payment model does not know its order, so we attach it here for the screens.
        payment.order_id = row["order_id"]
        payment.kind = row["kind"]
        return payment

    def insert_payment(self, conn, payment, order_id, kind, customer_id=None, bank_id=None):
        card = getattr(payment, "card_number", "")
        cursor = conn.execute(
            "INSERT INTO payment_transactions (kind, order_id, customer_id, bank_id, total_amount, "
            "card_last4, pay_date, pay_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (kind, order_id, customer_id, bank_id, payment.total_amount, card,
             payment.date.isoformat(), payment.time.isoformat()))
        return cursor.lastrowid

    def find_payment_by_id(self, conn, payment_id):
        row = conn.execute("SELECT * FROM payment_transactions WHERE id = ?",
                           (payment_id,)).fetchone()
        return self._to_payment(row) if row else None

    def find_payment_by_order(self, conn, order_id):
        row = conn.execute("SELECT * FROM payment_transactions WHERE order_id = ?",
                           (order_id,)).fetchone()
        return self._to_payment(row) if row else None

    def find_all_payments(self, conn):
        rows = conn.execute("SELECT * FROM payment_transactions ORDER BY id").fetchall()
        return [self._to_payment(row) for row in rows]
