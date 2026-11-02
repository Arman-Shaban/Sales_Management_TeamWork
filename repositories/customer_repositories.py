# SQL for customers. Every method receives an open connection from the service.
from models.customer import Customer


class CustomerRepository:

    def _to_customer(self, row):
        customer = Customer(row["name"], row["family"], row["phone"])
        customer.customer_id = row["id"]      # the real id comes from the database
        return customer

    def insert(self, conn, customer):
        cursor = conn.execute(
            "INSERT INTO customers (name, family, phone) VALUES (?, ?, ?)",
            (customer.customer_name, customer.customer_family, customer.customer_phone))
        return cursor.lastrowid

    def update(self, conn, customer):
        conn.execute(
            "UPDATE customers SET name = ?, family = ?, phone = ? WHERE id = ?",
            (customer.customer_name, customer.customer_family,
             customer.customer_phone, customer.customer_id))

    def delete(self, conn, customer_id):
        conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))

    def find_by_id(self, conn, customer_id):
        row = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
        return self._to_customer(row) if row else None

    def find_all(self, conn):
        rows = conn.execute("SELECT * FROM customers ORDER BY id").fetchall()
        return [self._to_customer(row) for row in rows]
