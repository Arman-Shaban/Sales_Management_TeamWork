# The main menu: one button for every screen.
from tkinter import Button, Label, Tk

from ui.views.customer_view import CustomerView
from ui.views.delivery_view import DeliveryView
from ui.views.inventory_view import InventoryView
from ui.views.order_item_view import OrderItemView
from ui.views.order_view import OrderView
from ui.views.payment_view import PaymentView
from ui.views.product_view import ProductView
from ui.views.transaction_inventory_view import TransactionInventoryView


class MainWindow:
    def __init__(self):
        self.win = Tk()
        self.win.title("Store Management System")
        self.win.geometry("320x420")

        Label(self.win, text="Store Management System", font=("Arial", 14, "bold")).pack(pady=15)

        screens = [
            ("Customers", CustomerView),
            ("Products", ProductView),
            ("Inventory", InventoryView),
            ("Inventory Transactions", TransactionInventoryView),
            ("Orders", OrderView),
            ("Order Items", OrderItemView),
            ("Payments", PaymentView),
            ("Deliveries", DeliveryView),
        ]
        for text, view_class in screens:
            Button(self.win, text=text, width=28,
                   command=lambda v=view_class: v(self.win)).pack(pady=4)

    def run(self):
        self.win.mainloop()
