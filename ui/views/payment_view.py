
from controller.payment_controller import PaymentController
from ui.widgets import (add_buttons, add_choice, add_field, fill_table, make_layout,
                        make_table, new_window, show_result, start)
from tkinter import Label


class PaymentView:
    def __init__(self, parent=None):
        self.controller = PaymentController()

        self.win = new_window(parent, "Payment", "900x460")
        form, table_frame = make_layout(self.win)

        self.order_id = add_field(form, "Order Id", 0)
        self.card_number = add_field(form, "Card Number", 1)
        self.bank = add_choice(form, "Bank (optional)", 2, [])
        add_buttons(form, 3, [("Pay", self.save_click), ("Clear", self.reset_form)])

        Label(form, text="New bank").grid(row=4, column=0, columnspan=2, pady=(15, 0))
        self.bank_name = add_field(form, "Bank Name", 5)
        self.branch_code = add_field(form, "Branch Code", 6)
        add_buttons(form, 7, [("Add Bank", self.add_bank_click)])

        self.table = make_table(table_frame,
                                ["Receipt No", "Order Id", "Kind", "Total", "Card (last 4)", "Date", "Time"],
                                [70, 60, 80, 80, 90, 90, 80])

        self.reset_form()
        start(self.win, parent)

    def load_banks(self):
        banks = self.controller.find_all_banks()[1]
        self.bank.combobox["values"] = [""] + [f"{b.bank_id} - {b.bank_name}" for b in banks]

    def reset_form(self):
        self.order_id.set("")
        self.card_number.set("")
        self.bank.set("")
        self.load_banks()
        rows = [(p.receipt_no, p.order_id, p.kind, p.total_amount,
                 getattr(p, "card_number", ""), p.date, p.time)
                for p in self.controller.find_all()[1]]
        fill_table(self.table, rows)

    def save_click(self):
        bank_id = self.bank.get().split(" - ")[0]      # "2 - Nordea" -> "2"
        success, message = self.controller.save(self.order_id.get(), self.card_number.get(), bank_id)
        if show_result(success, message):
            self.reset_form()

    def add_bank_click(self):
        success, message = self.controller.save_bank(self.bank_name.get(), self.branch_code.get())
        if show_result(success, message):
            self.bank_name.set("")
            self.branch_code.set("")
            self.load_banks()
