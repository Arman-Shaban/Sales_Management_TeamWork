
from controller.delivery_controller import DeliveryController
from ui.widgets import (add_buttons, add_field, fill_table, make_layout, make_table,
                        need_selection, new_window, selected_row, show_result, start)


class DeliveryView:
    def __init__(self, parent=None):
        self.controller = DeliveryController()

        self.win = new_window(parent, "Delivery", "960x420")
        form, table_frame = make_layout(self.win)

        self.delivery_id = add_field(form, "Delivery Id", 0, readonly=True)
        self.order_id = add_field(form, "Order Id", 1)
        self.address = add_field(form, "Address", 2)
        add_buttons(form, 3, [("Create", self.save_click), ("New", self.reset_form)])
        add_buttons(form, 4, [("Ship", self.ship_click), ("Deliver", self.deliver_click),
                              ("Cancel", self.cancel_click)])

        self.table = make_table(
            table_frame,
            ["Id", "Order Id", "Address", "Status", "Shipped At", "Delivered At"],
            [40, 60, 160, 80, 130, 130])
        self.table.bind("<<TreeviewSelect>>", self.table_click)

        self.reset_form()
        start(self.win, parent)

    def reset_form(self):
        self.delivery_id.set("")
        self.order_id.set("")
        self.address.set("")
        fill_table(self.table, [d.to_tuple() for d in self.controller.find_all()[1]])

    def save_click(self):
        success, message = self.controller.save(self.order_id.get(), self.address.get())
        if show_result(success, message):
            self.reset_form()

    def ship_click(self):
        self.change_delivery(self.controller.ship)

    def deliver_click(self):
        self.change_delivery(self.controller.deliver)

    def cancel_click(self):
        self.change_delivery(self.controller.cancel)

    def change_delivery(self, action):
        if not need_selection(self.delivery_id):
            return
        success, message = action(self.delivery_id.get())
        if show_result(success, message):
            self.reset_form()

    def table_click(self, event):
        row = selected_row(self.table)
        if row:
            self.delivery_id.set(row[0])
            self.order_id.set(row[1])
            self.address.set(row[2])
