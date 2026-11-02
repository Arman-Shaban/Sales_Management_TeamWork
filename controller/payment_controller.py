from controller.base import BaseController
from services.payment_service import PaymentService


class PaymentController(BaseController):
    def __init__(self, db=None):
        super().__init__(db)
        self.service = PaymentService(self.db)

    def save(self, order_id, card_number, bank_id):
        """Pay an order. bank_id may be empty."""
        def action():
            bank = self.to_int(bank_id, "Bank id") if str(bank_id).strip() else None
            self.service.pay_order(self.to_int(order_id, "Order id"), card_number, bank)
        return self.run(action, "Payment saved")

    def save_bank(self, name, branch_code):
        return self.run(lambda: self.service.add_bank(name, branch_code), "Bank saved")

    def find_all(self):
        return self.load(self.service.list_payments)

    def find_all_banks(self):
        return self.load(self.service.list_banks)
