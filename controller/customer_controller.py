from controller.base import BaseController
from services.customer_service import CustomerService


class CustomerController(BaseController):
    def __init__(self, db=None):
        super().__init__(db)
        self.service = CustomerService(self.db)

    def save(self, customer_id, name, family, phone):
        """customer_id 0 (or empty) = new customer, otherwise edit that customer."""
        def action():
            cid = self.to_int(customer_id or 0, "Customer id")
            if cid == 0:
                self.service.add(name, family, phone)
            else:
                self.service.update(cid, name, family, phone)
        return self.run(action, "Customer saved")

    def delete(self, customer_id):
        return self.run(lambda: self.service.delete(self.to_int(customer_id, "Customer id")),
                        "Customer deleted")

    def find_all(self):
        return self.load(self.service.list_all)
