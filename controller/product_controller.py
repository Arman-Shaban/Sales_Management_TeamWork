from controller.base import BaseController
from services.product_service import ProductService


class ProductController(BaseController):
    def __init__(self, db=None):
        super().__init__(db)
        self.service = ProductService(self.db)

    def save(self, product_id, product_name, product_brand, stock_inventory, price):
        """product_id 0 = new product. The stock is only used for a new product."""
        def action():
            pid = self.to_int(product_id or 0, "Product id")
            price_value = self.to_float(price, "Price")
            if pid == 0:
                self.service.add(product_name, product_brand, price_value,
                                 self.to_int(stock_inventory or 0, "Stock"))
            else:
                self.service.update(pid, product_name, product_brand, price_value)
        return self.run(action, "Product saved")

    def delete(self, product_id):
        return self.run(lambda: self.service.delete(self.to_int(product_id, "Product id")),
                        "Product deleted")

    def find_all(self):
        return self.load(self.service.list_all)
