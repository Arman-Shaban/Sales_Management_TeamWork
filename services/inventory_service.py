# Business rules for the inventory and the stock movements (inventory transactions).
from models.inventory import Inventory
from models.inventory_transaction import Inventory_Transaction
from repositories.inventory_repositories import InventoryRepository
from services.errors import BusinessRuleError, NotFoundError
from tools.helpers import now_text

# +1 = the stock grows, -1 = the stock shrinks
STOCK_DIRECTION = {"ADDITION": 1, "RETURN": 1, "CANCELLATION": 1, "SALE": -1}


class InventoryService:
    def __init__(self, db):
        self.db = db
        self.repo = InventoryRepository()

    # ----- methods that work inside a transaction opened by another service -----
    def create_inventory(self, conn, product_id, quantity=0, deficient_amount=5):
        """Create the inventory row of a new product (with a first ADDITION if quantity > 0)."""
        inventory = Inventory(0, product_id, 0, deficient_amount)
        inventory.inventory_id = self.repo.insert(conn, inventory)
        if quantity > 0:
            self.apply_transaction(conn, product_id, "ADDITION", quantity)
        return inventory

    def apply_transaction(self, conn, product_id, transaction_type, quantity, order_id=0):
        """Change the stock of a product and write the inventory transaction."""
        transaction = Inventory_Transaction(0, transaction_type, now_text(),
                                            product_id, quantity, order_id)   # validates the data
        inventory = self.repo.find_by_product(conn, product_id)
        if inventory is None:
            raise NotFoundError(f"Product {product_id} has no inventory")
        if order_id != 0 and conn.execute("SELECT 1 FROM orders WHERE id = ?",
                                          (order_id,)).fetchone() is None:
            raise NotFoundError(f"Order {order_id} was not found")

        new_quantity = inventory.inventory_quantity + STOCK_DIRECTION[transaction_type] * quantity
        if new_quantity < 0:
            raise BusinessRuleError(
                f"Not enough stock for product {product_id}: only {inventory.inventory_quantity} left")

        inventory.inventory_quantity = new_quantity
        inventory.inventory_date, inventory.inventory_time = now_text().split(" ")
        self.repo.update(conn, inventory)
        transaction.inventory_transaction_id = self.repo.insert_transaction(conn, transaction)
        return transaction

    # ----- methods used by the controllers -----
    def add_transaction(self, transaction_type, product_id, quantity, order_id=0):
        with self.db.transaction() as conn:
            return self.apply_transaction(conn, product_id, transaction_type, quantity, order_id)

    def update_deficient_amount(self, inventory_id, deficient_amount):
        with self.db.transaction() as conn:
            inventory = self.repo.find_by_id(conn, inventory_id)
            if inventory is None:
                raise NotFoundError(f"Inventory {inventory_id} was not found")
            inventory.deficient_amount = deficient_amount
            self.repo.update(conn, inventory)
            return inventory

    def get_by_product(self, product_id):
        with self.db.connection() as conn:
            inventory = self.repo.find_by_product(conn, product_id)
        if inventory is None:
            raise NotFoundError(f"Product {product_id} has no inventory")
        return inventory

    def list_all(self):
        with self.db.connection() as conn:
            return self.repo.find_all(conn)

    def list_low_stock(self):
        with self.db.connection() as conn:
            return self.repo.find_low_stock(conn)

    def list_transactions(self, product_id=None):
        with self.db.connection() as conn:
            if product_id is None:
                return self.repo.find_all_transactions(conn)
            return self.repo.find_transactions_by_product(conn, product_id)
