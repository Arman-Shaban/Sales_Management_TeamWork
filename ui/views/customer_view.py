
from controller.customer_controller import CustomerController
from ui.widgets import (add_buttons, add_field, fill_table, make_layout, make_table,
                        need_selection, new_window, selected_row, show_result, start)


class CustomerView:
    def __init__(self, parent=None):
        self.controller = CustomerController()

        self.win = new_window(parent, "Customer", "820x420")
        form, table_frame = make_layout(self.win)

        self.customer_id = add_field(form, "Customer Id", 0, readonly=True)
        self.name = add_field(form, "Name", 1)
        self.family = add_field(form, "Family", 2)
        self.phone = add_field(form, "Phone", 3)
        add_buttons(form, 4, [("Save", self.save_click), ("Delete", self.delete_click),
                              ("New", self.reset_form)])

        self.table = make_table(table_frame, ["Id", "Name", "Family", "Phone"],
                                [60, 130, 130, 130])
        self.table.bind("<<TreeviewSelect>>", self.table_click)

        self.reset_form()
        start(self.win, parent)

    def reset_form(self):
        self.customer_id.set("")
        self.name.set("")
        self.family.set("")
        self.phone.set("")
        rows = [(c.customer_id, c.customer_name, c.customer_family, c.customer_phone)
                for c in self.controller.find_all()[1]]
        fill_table(self.table, rows)

    def save_click(self):
        success, message = self.controller.save(self.customer_id.get(), self.name.get(),
                                                self.family.get(), self.phone.get())
        if show_result(success, message):
            self.reset_form()

    def delete_click(self):
        if not need_selection(self.customer_id):
            return
        success, message = self.controller.delete(self.customer_id.get())
        if show_result(success, message):
            self.reset_form()

    def table_click(self, event):
        row = selected_row(self.table)
        if row:
            self.customer_id.set(row[0])
            self.name.set(row[1])
            self.family.set(row[2])
            self.phone.set(row[3])
