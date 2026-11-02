# Business rules for orders and order items.
from models.order import Order
from models.order_item import Order_Item
from repositories.customer_repositories import CustomerRepository
from repositories.order_repositories import OrderRepository
from repositories.product_repositories import ProductRepository
from services.errors import BusinessRuleError, NotFoundError
from services.inventory_service import InventoryService
from tools.helpers import now_text


class OrderService:
    def __init__(self, db):
        self.db = db
        self.repo = OrderRepository()
        self.customer_repo = CustomerRepository()
        self.product_repo = ProductRepository()
        self.inventory_service = InventoryService(db)

    # ----- small helpers -----
    def _get_order(self, conn, order_id):
        order = self.repo.find_by_id(conn, order_id)
        if order is None:
            raise NotFoundError(f"Order {order_id} was not found")
        return order

    def _check_pending(self, order):
        if order.status != "pending":
            raise BusinessRuleError(f"Order {order.order_id} is {order.status}, it cannot be changed")

    def _recalculate(self, conn, order):
        """Total price and quantity of the order are always calculated from its items."""
        items = self.repo.find_items(conn, order.order_id)
        order.total_price = round(sum(item.price * item.quantity for item in items), 2)
        order.quantity = sum(item.quantity for item in items)
        self.repo.update(conn, order)

    # ----- orders -----
    def create_order(self, customer_id, order_type="sell"):
        with self.db.transaction() as conn:
            customer = self.customer_repo.find_by_id(conn, customer_id)
            if customer is None:
                raise NotFoundError(f"Customer {customer_id} was not found")
            full_name = f"{customer.customer_name} {customer.customer_family}"
            order = Order(0, order_type, customer.customer_id, full_name,
                          "pending", 0, 0, 0, 0, now_text())
            order.order_id = self.repo.insert(conn, order)
        return order

    def complete_order(self, order_id):
        """Confirm the order: the stock is reduced (sell) or increased (buy)."""
        with self.db.transaction() as conn:
            order = self._get_order(conn, order_id)
            self._check_pending(order)
            items = self.repo.find_items(conn, order_id)
            if not items:
                raise BusinessRuleError("The order has no items")

            if order.order_type == "cart":
                order.order_type = "sell"          # a confirmed basket is a sale
            transaction_type = "ADDITION" if order.order_type == "buy" else "SALE"

            last_transaction_id = 0
            for item in items:
                transaction = self.inventory_service.apply_transaction(
                    conn, item.product_id, transaction_type, item.quantity, order_id)
                last_transaction_id = transaction.inventory_transaction_id

            order.inventory_transaction_id = last_transaction_id   # the last stock movement
            order.status = "completed"
            self.repo.update(conn, order)
        return order

    def cancel_order(self, order_id):
        with self.db.transaction() as conn:
            order = self._get_order(conn, order_id)
            if order.status == "cancelled":
                raise BusinessRuleError("The order is already cancelled")

            if order.status == "completed":
                if order.order_type == "buy":
                    raise BusinessRuleError("A completed buy order cannot be cancelled")
                if order.payment_id != 0:
                    raise BusinessRuleError("A paid order cannot be cancelled")
                last_transaction_id = 0
                for item in self.repo.find_items(conn, order_id):     # give the goods back
                    transaction = self.inventory_service.apply_transaction(
                        conn, item.product_id, "CANCELLATION", item.quantity, order_id)
                    last_transaction_id = transaction.inventory_transaction_id
                order.inventory_transaction_id = last_transaction_id

            order.status = "cancelled"
            self.repo.update(conn, order)
        return order

    def delete_order(self, order_id):
        with self.db.transaction() as conn:
            order = self._get_order(conn, order_id)
            self._check_pending(order)
            self.repo.delete(conn, order_id)       # its items are deleted by the database

    def get_order(self, order_id):
        with self.db.connection() as conn:
            return self._get_order(conn, order_id)

    def list_orders(self):
        with self.db.connection() as conn:
            return self.repo.find_all(conn)

    # ----- order items -----
    def add_item(self, order_id, product_id, quantity):
        with self.db.transaction() as conn:
            order = self._get_order(conn, order_id)
            self._check_pending(order)
            product = self.product_repo.find_by_id(conn, product_id)
            if product is None:
                raise NotFoundError(f"Product {product_id} was not found")

            # creating the item validates the quantity and the other values
            new_item = Order_Item(0, order.customer_id, order.customer_name, product.product_id,
                                  product.product_name, product.price, quantity)

            existing = None
            for item in self.repo.find_items(conn, order_id):
                if item.product_id == product_id:
                    existing = item
            total_quantity = quantity + (existing.quantity if existing else 0)

            if order.order_type in ("sell", "cart") and total_quantity > product.stock_inventory:
                raise BusinessRuleError(
                    f"Not enough stock for {product.product_name}: only {product.stock_inventory} left")

            if existing:
                self.repo.update_item_quantity(conn, existing.order_item_id, total_quantity)
            else:
                new_item.order_item_id = self.repo.insert_item(conn, order_id, new_item)
            self._recalculate(conn, order)
        return order

    def remove_item(self, item_id):
        with self.db.transaction() as conn:
            order_id = self.repo.find_item_order_id(conn, item_id)
            if order_id is None:
                raise NotFoundError(f"Order item {item_id} was not found")
            order = self._get_order(conn, order_id)
            self._check_pending(order)
            self.repo.delete_item(conn, item_id)
            self._recalculate(conn, order)
        return order

    def list_items(self, order_id):
        with self.db.connection() as conn:
            self._get_order(conn, order_id)
            return self.repo.find_items(conn, order_id)
