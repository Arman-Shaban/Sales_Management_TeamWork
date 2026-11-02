from controller.base import BaseController
from services.delivery_service import DeliveryService


class DeliveryController(BaseController):
    def __init__(self, db=None):
        super().__init__(db)
        self.service = DeliveryService(self.db)

    def save(self, order_id, address):
        """Create the delivery of an order."""
        return self.run(lambda: self.service.create_delivery(
            self.to_int(order_id, "Order id"), address), "Delivery created")

    def ship(self, delivery_id):
        return self.run(lambda: self.service.ship(self.to_int(delivery_id, "Delivery id")),
                        "Delivery shipped")

    def deliver(self, delivery_id):
        return self.run(lambda: self.service.deliver(self.to_int(delivery_id, "Delivery id")),
                        "Delivery delivered")

    def cancel(self, delivery_id):
        return self.run(lambda: self.service.cancel(self.to_int(delivery_id, "Delivery id")),
                        "Delivery cancelled")

    def find_all(self):
        return self.load(self.service.list_all)
