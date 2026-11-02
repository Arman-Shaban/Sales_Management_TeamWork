#Sepideh
from controller.order_item_controller import OrderItemController
from ui.widgets import (add_buttons, add_field, fill_table, make_layout, make_table,
                        need_selection, new_window, selected_row, show_result, start)


class OrderItemView:
    def __init__(self, parent=None, order_id=""):
        self.controller = OrderItemController()

        self.win = new_window(parent, "Order Item", "900x420")
        form, table_frame = make_layout(self.win)

        self.order_id = add_field(form, "Order Id", 0)
        self.order_item_id = add_field(form, "Order Item Id", 1, readonly=True)
        self.product_id = add_field(form, "Product Id", 2)
        self.quantity = add_field(form, "Quantity", 3)
        self.total = add_field(form, "Items Total", 4, readonly=True)
        add_buttons(form, 5, [("Add Item", self.save_click), ("Remove Item", self.delete_click)])
        add_buttons(form, 6, [("Load Items", self.reset_form)])

        self.table = make_table(
            table_frame,
            ["Item Id", "Cust. Id", "Customer Name", "Product Id", "Product Name", "Quantity", "Price"],
            [50, 60, 120, 70, 120, 60, 70])
        self.table.bind("<<TreeviewSelect>>", self.table_click)

        self.order_id.set(order_id)
        self.reset_form()
        start(self.win, parent)

    def reset_form(self):
        """Show the items of the order that is written in the Order Id field."""
        self.order_item_id.set("")
        self.product_id.set("")
        self.quantity.set("")
        success, items = self.controller.find_by_order(self.order_id.get())
        fill_table(self.table, [item.to_tuple() for item in items])
        self.total.set(round(sum(item.price * item.quantity for item in items), 2))

    def save_click(self):
        success, message = self.controller.save(
            self.order_id.get(),
            self.product_id.get(),
            self.quantity.get())
        if show_result(success, message):
            self.reset_form()

    def delete_click(self):
        if not need_selection(self.order_item_id):
            return
        success, message = self.controller.delete(self.order_item_id.get())
        if show_result(success, message):
            self.reset_form()

    def table_click(self, event):
        row = selected_row(self.table)
        if row:
            self.order_item_id.set(row[0])
            self.product_id.set(row[3])
            self.quantity.set(row[5])
