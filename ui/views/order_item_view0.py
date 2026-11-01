#Sepideh
from tkinter import *
from tkinter import ttk ,messagebox

from controller.order_utem_controller import OrderItemController


class OrderItemView:
    def __init__(self):
        self.controller = OrderItemController()

        self.win = Tk()
        self.win.geometry("600x350")
        self.win.title("OrderItem")

        # OrderItemID
        Label(self.win, text="Order Item Id").place(x=20,y=20)
        self.order_item_id = IntVar()
        Entry(self.win, textvariable=self.order_item_id).place(x=100, y = 20)

        # CustomerName
        Label(self.win, text="Customer Name").place(x=20, y=60)
        self.customer_name = StrVar()
        Entry(self.win, textvariable=self.customer_name).place(x=100, y=60)

        # ProductID
        Label(self.win, text="Product Id").place(x=20,y=100)
        self.product_id = IntVar()
        Entry(self.win, textvariable=self.product_id).place(x=100, y = 100)

        # ProductName
        Label(self.win, text="Product Name").place(x=20, y=140)
        self.Product_name = StrVar()
        Entry(self.win, textvariable=self.Product_name).place(x=100, y=140)

        # Quantity
        Label(self.win, text="Quantity").place(x=20,y=180)
        self.quantity = IntVar()
        Entry(self.win, textvariable=self.quantity).place(x=100, y = 180)

        # Price
        Label(self.win, text="Price").place(x=20,y=220)
        self.price = IntVar()
        Entry(self.win, textvariable=self.price).place(x=100, y = 220)


        # table
        self.table = ttk.Treeview(self.win, show="headings", columns=[1,2,3,4,5,6])
        self.table.place(x=250, y =20)

        self.table.column(1, width=60)
        self.table.column(2, width=100)
        self.table.column(3, width=60)
        self.table.column(4, width=100)
        self.table.column(5, width=60)
        self.table.column(6, width=60)


        self.table.heading(1, text="Order Item Id")
        self.table.heading(2, text="Customer Name")
        self.table.heading(3, text="Product Id")
        self.table.heading(4, text="Product Name")
        self.table.heading(5, text="Quantity")
        self.table.heading(6, text="Price")



        self.table.bind("<ButtonRelease>", self.table_click)

        Button(self.win, text="Save", command=self.save_click).place(x= 50, y = 200)
        self.reset_from()
        self.win.mainloop()


    def reset_from(self):
        self.order_item_id.set(0)
        self.customer_name.set("")
        self.product_id.set(0)
        self.Product_name.set("")
        self.quantity.set(0)
        self.price.set(0)


        # Clear Table
        for item in self.table.get_children():
            self.table.delete(item)

        # Set All OrderItem On Table
        for OrderItem in self.controller.find_all()[1]:
            self.table.insert("", END, values=OrderItem.to_tuple())


    def save_click(self):
        success, message = self.controller.save(
            self.order_id.get(),
            self.customer_name.get(),
            self.product_id.get(),
            self.Product_name.get(),
            self.quantity.get(),
            self.price.get()
        )

        if success:
            messagebox.showinfo("Success", message)
            self.reset_from()
        else:
            messagebox.showerror("Error", message)


    def table_click(self, event):
        selected_order_item_id = self.table.focus()
        selected_order_item_id = self.table.item(selected_order_item_id)["values"]

        if selected_order_item:
            self.order_id.set(int(selected_order_item[0]))
            self.customer_name.set(int(selected_order_item[1]))
            self.product_id.set(int(selected_order_item[2]))
            self.Product_name.set(int(selected_order_item[3]))
            self.quantity.set(int(selected_order_item[4]))
            self.price.set(int(selected_order_item[5]))
            
