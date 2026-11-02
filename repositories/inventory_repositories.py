# SQL for the inventory table and the inventory_transactions table.
from models.inventory import Inventory
from models.inventory_transaction import Inventory_Transaction


class InventoryRepository:

    def _to_inventory(self, row):
        return Inventory(row["id"], row["product_id"], row["quantity"],
                         row["deficient_amount"], row["inventory_time"], row["inventory_date"])

    def _to_transaction(self, row):
        return Inventory_Transaction(row["id"], row["type"], row["date_time"],
                                     row["product_id"], row["quantity"], row["order_id"])

    # ----- inventory -----
    def insert(self, conn, inventory):
        cursor = conn.execute(
            "INSERT INTO inventory (product_id, quantity, deficient_amount, inventory_date, inventory_time) "
            "VALUES (?, ?, ?, ?, ?)",
            (inventory.product_id, inventory.inventory_quantity, inventory.deficient_amount,
             inventory.inventory_date, inventory.inventory_time))
        return cursor.lastrowid

    def update(self, conn, inventory):
        conn.execute(
            "UPDATE inventory SET quantity = ?, deficient_amount = ?, "
            "inventory_date = ?, inventory_time = ? WHERE id = ?",
            (inventory.inventory_quantity, inventory.deficient_amount,
             inventory.inventory_date, inventory.inventory_time, inventory.inventory_id))

    def find_by_id(self, conn, inventory_id):
        row = conn.execute("SELECT * FROM inventory WHERE id = ?", (inventory_id,)).fetchone()
        return self._to_inventory(row) if row else None

    def find_by_product(self, conn, product_id):
        row = conn.execute("SELECT * FROM inventory WHERE product_id = ?", (product_id,)).fetchone()
        return self._to_inventory(row) if row else None

    def find_all(self, conn):
        rows = conn.execute("SELECT * FROM inventory ORDER BY id").fetchall()
        return [self._to_inventory(row) for row in rows]

    def find_low_stock(self, conn):
        rows = conn.execute(
            "SELECT * FROM inventory WHERE quantity <= deficient_amount ORDER BY id").fetchall()
        return [self._to_inventory(row) for row in rows]

    # ----- transactions -----
    def insert_transaction(self, conn, transaction):
        cursor = conn.execute(
            "INSERT INTO inventory_transactions (type, date_time, product_id, quantity, order_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (transaction.inventory_transaction_type, transaction.inventory_transaction_datetime,
             transaction.product_id, transaction.quantity, transaction.order_id))
        return cursor.lastrowid

    def find_all_transactions(self, conn):
        rows = conn.execute("SELECT * FROM inventory_transactions ORDER BY id").fetchall()
        return [self._to_transaction(row) for row in rows]

    def find_transactions_by_product(self, conn, product_id):
        rows = conn.execute(
            "SELECT * FROM inventory_transactions WHERE product_id = ? ORDER BY id",
            (product_id,)).fetchall()
        return [self._to_transaction(row) for row in rows]
