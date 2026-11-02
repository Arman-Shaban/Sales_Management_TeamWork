# Business rules for deliveries.
from models.delivery import Delivery
from repositories.delivery_repositories import DeliveryRepository
from repositories.order_repositories import OrderRepository
from services.errors import BusinessRuleError, NotFoundError
from tools.helpers import now_text


class DeliveryService:
    def __init__(self, db):
        self.db = db
        self.repo = DeliveryRepository()
        self.order_repo = OrderRepository()

    def _get(self, conn, delivery_id):
        delivery = self.repo.find_by_id(conn, delivery_id)
        if delivery is None:
            raise NotFoundError(f"Delivery {delivery_id} was not found")
        return delivery

    def create_delivery(self, order_id, address):
        with self.db.transaction() as conn:
            order = self.order_repo.find_by_id(conn, order_id)
            if order is None:
                raise NotFoundError(f"Order {order_id} was not found")
            if order.order_type != "sell" or order.status != "completed":
                raise BusinessRuleError("Only completed sell orders can be delivered")
            if self.repo.find_by_order(conn, order_id) is not None:
                raise BusinessRuleError("This order already has a delivery")
            delivery = Delivery(0, order_id, address.strip(), "pending")
            delivery.delivery_id = self.repo.insert(conn, delivery)
        return delivery

    def ship(self, delivery_id):
        with self.db.transaction() as conn:
            delivery = self._get(conn, delivery_id)
            if delivery.status != "pending":
                raise BusinessRuleError("Only pending deliveries can be shipped")
            order = self.order_repo.find_by_id(conn, delivery.order_id)
            if order.payment_id == 0:
                raise BusinessRuleError("The order must be paid before it is shipped")
            delivery.status = "shipped"
            delivery.shipped_at = now_text()
            self.repo.update(conn, delivery)
        return delivery

    def deliver(self, delivery_id):
        with self.db.transaction() as conn:
            delivery = self._get(conn, delivery_id)
            if delivery.status != "shipped":
                raise BusinessRuleError("Only shipped deliveries can be delivered")
            delivery.status = "delivered"
            delivery.delivered_at = now_text()
            self.repo.update(conn, delivery)
        return delivery

    def cancel(self, delivery_id):
        with self.db.transaction() as conn:
            delivery = self._get(conn, delivery_id)
            if delivery.status != "pending":
                raise BusinessRuleError("Only pending deliveries can be cancelled")
            delivery.status = "cancelled"
            self.repo.update(conn, delivery)
        return delivery

    def get(self, delivery_id):
        with self.db.connection() as conn:
            return self._get(conn, delivery_id)

    def list_all(self):
        with self.db.connection() as conn:
            return self.repo.find_all(conn)
