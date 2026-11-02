from controller.base import BaseController
from services.inventory_service import InventoryService


class TransactionInventoryController(BaseController):
    def __init__(self, db=None):
        super().__init__(db)
        self.service = InventoryService(self.db)

    def save(self, transaction_type, product_id, order_id, quantity):
        """Create a new stock movement (the date and time are set automatically)."""
        def action():
            self.service.add_transaction(
                transaction_type.strip().upper(),
                self.to_int(product_id, "Product id"),
                self.to_int(quantity, "Quantity"),
                self.to_int(order_id or 0, "Order id"))
        return self.run(action, "Inventory transaction saved")

    def find_all(self):
        return self.load(self.service.list_transactions)
