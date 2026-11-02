# SQL for deliveries.
from models.delivery import Delivery


class DeliveryRepository:

    def _to_delivery(self, row):
        return Delivery(row["id"], row["order_id"], row["address"], row["status"],
                        row["shipped_at"], row["delivered_at"])

    def insert(self, conn, delivery):
        cursor = conn.execute(
            "INSERT INTO deliveries (order_id, address, status) VALUES (?, ?, ?)",
            (delivery.order_id, delivery.address, delivery.status))
        return cursor.lastrowid

    def update(self, conn, delivery):
        conn.execute(
            "UPDATE deliveries SET address = ?, status = ?, shipped_at = ?, delivered_at = ? "
            "WHERE id = ?",
            (delivery.address, delivery.status, delivery.shipped_at,
             delivery.delivered_at, delivery.delivery_id))

    def find_by_id(self, conn, delivery_id):
        row = conn.execute("SELECT * FROM deliveries WHERE id = ?", (delivery_id,)).fetchone()
        return self._to_delivery(row) if row else None

    def find_by_order(self, conn, order_id):
        row = conn.execute("SELECT * FROM deliveries WHERE order_id = ?", (order_id,)).fetchone()
        return self._to_delivery(row) if row else None

    def find_all(self, conn):
        rows = conn.execute("SELECT * FROM deliveries ORDER BY id").fetchall()
        return [self._to_delivery(row) for row in rows]
