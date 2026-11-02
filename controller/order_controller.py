from controller.base import BaseController
from services.order_service import OrderService


class OrderController(BaseController):
    def __init__(self, db=None):
        super().__init__(db)
        self.service = OrderService(self.db)

    def save(self, order_type, customer_id):
        """Create a new empty order. Items are added in the order item screen."""
        def action():
            self.service.create_order(self.to_int(customer_id, "Customer id"),
                                      order_type.strip().lower())
        return self.run(action, "Order created")

    def complete(self, order_id):
        return self.run(lambda: self.service.complete_order(self.to_int(order_id, "Order id")),
                        "Order completed")

    def cancel(self, order_id):
        return self.run(lambda: self.service.cancel_order(self.to_int(order_id, "Order id")),
                        "Order cancelled")

    def delete(self, order_id):
        return self.run(lambda: self.service.delete_order(self.to_int(order_id, "Order id")),
                        "Order deleted")

    def find_all(self):
        return self.load(self.service.list_orders)
