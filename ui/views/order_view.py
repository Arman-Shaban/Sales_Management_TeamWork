#Sepideh
from controller.order_controller import OrderController
from tools.validation import Validator
from ui.widgets import (add_buttons, add_choice, add_field, fill_table, make_layout,
                        make_table, need_selection, new_window, selected_row, show_result, start)


class OrderView:
    def __init__(self, parent=None):
        self.controller = OrderController()

        self.win = new_window(parent, "Order", "1250x460")
        form, table_frame = make_layout(self.win)

        self.order_id = add_field(form, "Order Id", 0, readonly=True)
        self.order_type = add_choice(form, "Order Type", 1, list(Validator.ORDER_TYPES))
        self.customer_id = add_field(form, "Customer Id", 2)
        self.status = add_field(form, "Status", 3, readonly=True)
        self.total_price = add_field(form, "Total Price", 4, readonly=True)
        add_buttons(form, 5, [("Create", self.save_click), ("Items", self.items_click)])
        add_buttons(form, 6, [("Complete", self.complete_click), ("Cancel", self.cancel_click),
                              ("Delete", self.delete_click)])

        self.table = make_table(
            table_frame,
            ["Order Id", "Type", "Cust. Id", "Customer Name", "Status", "Total Price",
             "Payment Id", "Inv. Trans. Id", "Quantity", "DateTime", "OrderTime"],
            [60, 50, 60, 120, 80, 80, 70, 80, 60, 130, 130])
        self.table.bind("<<TreeviewSelect>>", self.table_click)

        self.reset_form()
        start(self.win, parent)

    def reset_form(self):
        self.order_id.set("")
        self.order_type.set("sell")
        self.customer_id.set("")
        self.status.set("")
        self.total_price.set("")
        fill_table(self.table, [o.to_tuple() for o in self.controller.find_all()[1]])

    def save_click(self):
        """Create a new order. Products are added with the Items button."""
        success, message = self.controller.save(self.order_type.get(), self.customer_id.get())
        if show_result(success, message):
            self.reset_form()

    def complete_click(self):
        self.change_order(self.controller.complete)

    def cancel_click(self):
        self.change_order(self.controller.cancel)

    def delete_click(self):
        self.change_order(self.controller.delete)

    def change_order(self, action):
        if not need_selection(self.order_id):
            return
        success, message = action(self.order_id.get())
        if show_result(success, message):
            self.reset_form()

    def items_click(self):
        if not need_selection(self.order_id):
            return
        from ui.views.order_item_view import OrderItemView   # imported here to avoid a loop
        OrderItemView(self.win, self.order_id.get())

    def table_click(self, event):
        row = selected_row(self.table)
        if row:
            self.order_id.set(row[0])
            self.order_type.set(row[1])
            self.customer_id.set(row[2])
            self.status.set(row[4])
            self.total_price.set(row[5])
