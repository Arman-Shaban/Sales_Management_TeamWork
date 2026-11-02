# Business rules for products.
import sqlite3

from models.product import Product
from repositories.product_repositories import ProductRepository
from services.errors import BusinessRuleError, NotFoundError
from services.inventory_service import InventoryService


class ProductService:
    def __init__(self, db):
        self.db = db
        self.repo = ProductRepository()
        self.inventory_service = InventoryService(db)

    def add(self, name, brand, price, stock=0):
        product = Product(0, name.strip(), brand.strip(), stock, price)   # validates the data
        with self.db.transaction() as conn:
            product.product_id = self.repo.insert(conn, product)
            self.inventory_service.create_inventory(conn, product.product_id, stock)
        return product

    def update(self, product_id, name, brand, price):
        """The stock is not changed here, use an inventory transaction for that."""
        with self.db.transaction() as conn:
            product = self.repo.find_by_id(conn, product_id)
            if product is None:
                raise NotFoundError(f"Product {product_id} was not found")
            product.product_name = name.strip()
            product.product_brand = brand.strip()
            product.price = price
            self.repo.update(conn, product)
        return product

    def delete(self, product_id):
        try:
            with self.db.transaction() as conn:
                if self.repo.find_by_id(conn, product_id) is None:
                    raise NotFoundError(f"Product {product_id} was not found")
                self.repo.delete(conn, product_id)
        except sqlite3.IntegrityError:
            raise BusinessRuleError("This product is used in orders and cannot be deleted")

    def get(self, product_id):
        with self.db.connection() as conn:
            product = self.repo.find_by_id(conn, product_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} was not found")
        return product

    def list_all(self):
        with self.db.connection() as conn:
            return self.repo.find_all(conn)
