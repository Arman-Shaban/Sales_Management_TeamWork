from controller.base import BaseController
from services.order_service import OrderService


class OrderItemController(BaseController):
    def __init__(self, db=None):
        super().__init__(db)
        self.service = OrderService(self.db)

    def save(self, order_id, product_id, quantity):
        """Add a product to an order (the same product again increases the quantity)."""
        def action():
            self.service.add_item(self.to_int(order_id, "Order id"),
                                  self.to_int(product_id, "Product id"),
                                  self.to_int(quantity, "Quantity"))
        return self.run(action, "Item saved")

    def delete(self, order_item_id):
        return self.run(lambda: self.service.remove_item(self.to_int(order_item_id, "Order item id")),
                        "Item removed")

    def find_by_order(self, order_id):
        return self.load(lambda: self.service.list_items(self.to_int(order_id, "Order id")))
