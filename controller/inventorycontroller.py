from controller.base import BaseController
from services.inventory_service import InventoryService


class InventoryController(BaseController):
    def __init__(self, db=None):
        super().__init__(db)
        self.service = InventoryService(self.db)

    def save(self, inventory_id, deficient_amount):
        """Only the low-stock limit can be edited here; the quantity changes through
        inventory transactions."""
        def action():
            self.service.update_deficient_amount(
                self.to_int(inventory_id, "Inventory id"),
                self.to_int(deficient_amount, "Deficient amount"))
        return self.run(action, "Inventory saved")

    def find_all(self):
        return self.load(self.service.list_all)

    def find_low_stock(self):
        return self.load(self.service.list_low_stock)
