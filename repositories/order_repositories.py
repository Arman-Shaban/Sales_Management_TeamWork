# SQL for orders and order items.
from models.order import Order
from models.order_item import Order_Item


class OrderRepository:

    def _to_order(self, row):
        return Order(row["id"], row["order_type"], row["customer_id"], row["customer_name"],
                     row["status"], row["total_price"], row["quantity"], row["payment_id"],
                     row["inventory_transaction_id"], row["date_time"], row["order_time"])

    def _to_item(self, row):
        return Order_Item(row["id"], row["customer_id"], row["customer_name"],
                          row["product_id"], row["product_name"], row["price"], row["quantity"])

    # ----- orders -----
    def insert(self, conn, order):
        cursor = conn.execute(
            "INSERT INTO orders (order_type, customer_id, customer_name, status, total_price, "
            "quantity, payment_id, inventory_transaction_id, date_time, order_time) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (order.order_type, order.customer_id, order.customer_name, order.status,
             order.total_price, order.quantity, order.payment_id,
             order.inventory_transaction_id, order.date_time, order.order_time))
        return cursor.lastrowid

    def update(self, conn, order):
        conn.execute(
            "UPDATE orders SET order_type = ?, status = ?, total_price = ?, quantity = ?, "
            "payment_id = ?, inventory_transaction_id = ? WHERE id = ?",
            (order.order_type, order.status, order.total_price, order.quantity,
             order.payment_id, order.inventory_transaction_id, order.order_id))

    def delete(self, conn, order_id):
        conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))

    def find_by_id(self, conn, order_id):
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        return self._to_order(row) if row else None

    def find_all(self, conn):
        rows = conn.execute("SELECT * FROM orders ORDER BY id").fetchall()
        return [self._to_order(row) for row in rows]

    # ----- order items (the Order_Item model has no order id, so it is passed separately) -----
    def insert_item(self, conn, order_id, item):
        cursor = conn.execute(
            "INSERT INTO order_items (order_id, customer_id, customer_name, product_id, "
            "product_name, price, quantity) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (order_id, item.customer_id, item.customer_name, item.product_id,
             item.product_name, item.price, item.quantity))
        return cursor.lastrowid

    def update_item_quantity(self, conn, item_id, quantity):
        conn.execute("UPDATE order_items SET quantity = ? WHERE id = ?", (quantity, item_id))

    def delete_item(self, conn, item_id):
        conn.execute("DELETE FROM order_items WHERE id = ?", (item_id,))

    def find_item(self, conn, item_id):
        row = conn.execute("SELECT * FROM order_items WHERE id = ?", (item_id,)).fetchone()
        return self._to_item(row) if row else None

    def find_item_order_id(self, conn, item_id):
        row = conn.execute("SELECT order_id FROM order_items WHERE id = ?", (item_id,)).fetchone()
        return row["order_id"] if row else None

    def find_items(self, conn, order_id):
        rows = conn.execute(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY id", (order_id,)).fetchall()
        return [self._to_item(row) for row in rows]
