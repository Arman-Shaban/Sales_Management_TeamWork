#Sepideh
from controller.transaction_inventorycontroller import TransactionInventoryController
from tools.validation import Validator
from ui.widgets import (add_buttons, add_choice, add_field, fill_table, make_layout,
                        make_table, new_window, show_result, start)


class TransactionInventoryView:
    def __init__(self, parent=None):
        self.controller = TransactionInventoryController()

        self.win = new_window(parent, "Transaction Inventory", "860x420")
        form, table_frame = make_layout(self.win)

        self.transaction_type = add_choice(form, "Transaction Type", 0,
                                           list(Validator.TRANSACTION_TYPES))
        self.product_id = add_field(form, "Product Id", 1)
        self.order_id = add_field(form, "Order Id (0 = none)", 2)
        self.quantity = add_field(form, "Quantity", 3)
        add_buttons(form, 4, [("Save", self.save_click), ("New", self.reset_form)])

        self.table = make_table(table_frame,
                                ["Id", "Type", "Datetime", "Quantity", "Product Id", "Order Id"],
                                [40, 100, 140, 60, 70, 60])

        self.reset_form()
        start(self.win, parent)

    def reset_form(self):
        self.transaction_type.set("ADDITION")
        self.product_id.set("")
        self.order_id.set("0")
        self.quantity.set("")
        fill_table(self.table, [t.to_tuple() for t in self.controller.find_all()[1]])

    def save_click(self):
        success, message = self.controller.save(
            self.transaction_type.get(),
            self.product_id.get(),
            self.order_id.get(),
            self.quantity.get())
        if show_result(success, message):
            self.reset_form()
