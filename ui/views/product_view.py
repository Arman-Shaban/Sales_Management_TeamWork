#Sepideh
from controller.product_controller import ProductController
from ui.widgets import (add_buttons, add_field, fill_table, make_layout, make_table,
                        need_selection, new_window, selected_row, show_result, start)
from tkinter import Label


class ProductView:
    def __init__(self, parent=None):
        self.controller = ProductController()

        self.win = new_window(parent, "Product", "820x420")
        form, table_frame = make_layout(self.win)

        self.product_id = add_field(form, "Product Id", 0, readonly=True)
        self.product_name = add_field(form, "Product Name", 1)
        self.product_brand = add_field(form, "Product Brand", 2)
        self.stock_inventory = add_field(form, "Stock Inventory", 3)
        self.price = add_field(form, "Price", 4)
        Label(form, text="Stock is only used for a new product.\nChange it later with an "
                         "inventory transaction.", justify="left").grid(row=5, column=0,
                                                                         columnspan=2)
        add_buttons(form, 6, [("Save", self.save_click), ("Delete", self.delete_click),
                              ("New", self.reset_form)])

        self.table = make_table(table_frame, ["Product Id", "Product Name", "Brand", "Stock", "Price"],
                                [70, 130, 100, 60, 70])
        self.table.bind("<<TreeviewSelect>>", self.table_click)

        self.reset_form()
        start(self.win, parent)

    def reset_form(self):
        self.product_id.set("")
        self.product_name.set("")
        self.product_brand.set("")
        self.stock_inventory.set("0")
        self.price.set("")
        fill_table(self.table, [p.to_tuple() for p in self.controller.find_all()[1]])

    def save_click(self):
        success, message = self.controller.save(
            self.product_id.get(),
            self.product_name.get(),
            self.product_brand.get(),
            self.stock_inventory.get(),
            self.price.get())
        if show_result(success, message):
            self.reset_form()

    def delete_click(self):
        if not need_selection(self.product_id):
            return
        success, message = self.controller.delete(self.product_id.get())
        if show_result(success, message):
            self.reset_form()

    def table_click(self, event):
        row = selected_row(self.table)
        if row:
            self.product_id.set(row[0])
            self.product_name.set(row[1])
            self.product_brand.set(row[2])
            self.stock_inventory.set(row[3])
            self.price.set(row[4])
