# SQL for products. The stock comes from the inventory table (LEFT JOIN).
from models.product import Product

SELECT_PRODUCT = """
    SELECT p.id, p.name, p.brand, p.price, COALESCE(i.quantity, 0) AS stock
    FROM products p LEFT JOIN inventory i ON i.product_id = p.id
"""


class ProductRepository:

    def _to_product(self, row):
        return Product(row["id"], row["name"], row["brand"], row["stock"], row["price"])

    def insert(self, conn, product):
        cursor = conn.execute(
            "INSERT INTO products (name, brand, price) VALUES (?, ?, ?)",
            (product.product_name, product.product_brand, product.price))
        return cursor.lastrowid

    def update(self, conn, product):
        conn.execute(
            "UPDATE products SET name = ?, brand = ?, price = ? WHERE id = ?",
            (product.product_name, product.product_brand, product.price, product.product_id))

    def delete(self, conn, product_id):
        conn.execute("DELETE FROM products WHERE id = ?", (product_id,))

    def find_by_id(self, conn, product_id):
        row = conn.execute(SELECT_PRODUCT + " WHERE p.id = ?", (product_id,)).fetchone()
        return self._to_product(row) if row else None

    def find_all(self, conn):
        rows = conn.execute(SELECT_PRODUCT + " ORDER BY p.id").fetchall()
        return [self._to_product(row) for row in rows]
