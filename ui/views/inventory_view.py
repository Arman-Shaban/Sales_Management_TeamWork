#Sepideh
from tkinter import Button

from controller.inventorycontroller import InventoryController
from ui.widgets import (add_buttons, add_field, fill_table, make_layout, make_table,
                        need_selection, new_window, selected_row, show_result, start)


class InventoryView:
    def __init__(self, parent=None):
        self.controller = InventoryController()
        self.only_low = False

        self.win = new_window(parent, "Inventory", "760x420")
        form, table_frame = make_layout(self.win)

        self.inventory_id = add_field(form, "Inventory Id", 0, readonly=True)
        self.product_id = add_field(form, "Product Id", 1, readonly=True)
        self.inventory_quantity = add_field(form, "Inventory Quantity", 2, readonly=True)
        self.deficient_amount = add_field(form, "Deficient Amount", 3)
        add_buttons(form, 4, [("Save", self.save_click), ("Show All", self.show_all),
                              ("Low Stock", self.show_low)])

        self.table = make_table(table_frame,
                                ["Inventory Id", "Quantity", "Product Id", "Deficient Amount"],
                                [80, 70, 80, 110])
        self.table.bind("<<TreeviewSelect>>", self.table_click)

        self.reset_form()
        start(self.win, parent)

    def reset_form(self):
        self.inventory_id.set("")
        self.product_id.set("")
        self.inventory_quantity.set("")
        self.deficient_amount.set("")
        if self.only_low:
            inventories = self.controller.find_low_stock()[1]
        else:
            inventories = self.controller.find_all()[1]
        # rows with quantity <= deficient amount are shown in red
        fill_table(self.table, [i.to_tuple() for i in inventories],
                   is_low=lambda row: row[1] <= row[3])

    def show_all(self):
        self.only_low = False
        self.reset_form()

    def show_low(self):
        self.only_low = True
        self.reset_form()

    def save_click(self):
        if not need_selection(self.inventory_id):
            return
        success, message = self.controller.save(self.inventory_id.get(), self.deficient_amount.get())
        if show_result(success, message):
            self.reset_form()

    def table_click(self, event):
        row = selected_row(self.table)
        if row:
            self.inventory_id.set(row[0])
            self.inventory_quantity.set(row[1])
            self.product_id.set(row[2])
            self.deficient_amount.set(row[3])
