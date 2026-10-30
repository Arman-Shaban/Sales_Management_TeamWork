#Nastaran

class Customer:

    next_id = 1001

    def __init__(self, customer_name, customer_family, customer_phone):
        self.customer_id = Customer.next_id
        Customer.next_id += 1
        self.customer_name = customer_name
        self.customer_family = customer_family
        self.customer_phone = customer_phone

    def __repr__(self):
        return f"Customer(id = {self.customer_id}, name = {self.customer_name}, family = {self.customer_family}, phone = {self.customer_phone})"


    def validate_information(self):
        attempt = 0
        while attempt < 3:
            print("Do You Confirm the Above Information?")
            confirmation =input("Enter Yes Or No: ")
            if confirmation == "Yes":
                print(f"Hello Dear {self.customer_name}")
                return True
            else:
                print("Please Edit Your Information")
                self.editing()
                attempt +=1
        print("Error: Too Many Attempt! ")
        return False

    def editing(self):
        print("Which information would you like to edit? ")
        editing = input("name or family or phone? ")
        if editing == "name":
            self.customer_name = input(" Enter Your Name: ")
        elif editing == "family":
            self.customer_family = input(" Enter Your family: ")
        elif editing == "phone":
            self.customer_phone = input(" Enter Your phone: ")
        else:
            print(" Error: Invalid Option")

        print(f"Customer(id = {self.customer_id}, name = {self.customer_name}, family = {self.customer_family}, phone = {self.customer_phone})")




name = input(" Enter Your Name: ")
family = input(" Enter Your Family: ")
phone = input(" Enter Your Phone: ")
customer1 = Customer(name, family, phone)
print(customer1)
customer1.validate_information()
