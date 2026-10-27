#Nastaran

class Customer:

    next_id = 1

    def __init__(self, customer_name, customer_family, customer_phone):
        self.customer_id = Customer.next_id
        Customer.next_id += 1
        self.customer_name = customer_name
        self.customer_family = customer_family
        self.customer_phone = customer_phone

    def __repr__(self):
        return f"Customer(id = {self.customer_id}, name = {self.customer_name}, family = {self.customer_family}, phone = {self.customer_phone})"

    def validate_information(self):
        print("Do You Confirm the Above Information?")
        confirmation =input("Enter Yes Or No: ")
        if confirmation == "Yes":
            print(f"Hello Dear {self.customer_name}")
        if confirmation =="No":
            print("Please Edit Your Information")

    def editing(self):
        print("Which information would you like to edit? ")
        editing = input("name or family or phone? ")
        if editing == "name":
            self.customer_name =input(" Enter Your Name: ")
        if editing == "family":
            self.customer_family =input(" Enter Your family: ")
        if editing == "phone":
            self.customer_phone =input(" Enter Your phone: ")
        print(f" Hello Dear {self.customer_name}")


name = input(" Enter Your Name: ")
family = input(" Enter Your Family: ")
phone = input(" Enter Your Phone: ")
customer1 = Customer(name, family, phone)
print(customer1)
customer1.validate_information()
customer1.editing()