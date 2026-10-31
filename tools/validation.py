# ARMAN UPDATE 10/31/2026


# Validation rules used by the models and the services.
# Every method raises ValueError with a clear message when the value is wrong.
from datetime import datetime

from tools.helpers import DATETIME_FORMAT


class Validator:
    ORDER_TYPES = ("buy", "sell", "cart")
    ORDER_STATUSES = ("pending", "completed", "cancelled")
    TRANSACTION_TYPES = ("ADDITION", "SALE", "RETURN", "CANCELLATION")
    DELIVERY_STATUSES = ("pending", "shipped", "delivered", "cancelled")

# ---------- basic helpers ----------
    @staticmethod
    def _whole_number(value, label, minimum=0):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{label} must be a whole number")
        if value < minimum:
            raise ValueError(f"{label} must be at least {minimum}")

    @staticmethod
    def _text(value, label, max_length=100):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} cannot be empty")
        if len(value) > max_length:
            raise ValueError(f"{label} is too long (max {max_length} characters)")

    @staticmethod
    def _money(value, label, allow_zero):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{label} must be a number")
        if value < 0 or (value == 0 and not allow_zero):
            raise ValueError(f"{label} must be greater than 0" if not allow_zero
                             else f"{label} cannot be negative")

    @staticmethod
    def _choice(value, label, allowed):
        if value not in allowed:
            raise ValueError(f"{label} must be one of: {', '.join(allowed)}")

    @staticmethod
    def _date_text(value, label):
        try:
            datetime.strptime(value, DATETIME_FORMAT)
        except (TypeError, ValueError):
            raise ValueError(f"{label} must look like 2026-10-31 14:30:00")

# ---------- ids (0 means "not saved yet") ----------
    @staticmethod
    def inventory_id_validator(value):
        Validator._whole_number(value, "Inventory id")

    @staticmethod
    def product_id_validator(value):
        Validator._whole_number(value, "Product id")

    @staticmethod
    def order_id_validator(value):
        Validator._whole_number(value, "Order id")

    @staticmethod
    def order_item_id_validator(value):
        Validator._whole_number(value, "Order item id")

    @staticmethod
    def customer_id_validator(value):
        Validator._whole_number(value, "Customer id")

    @staticmethod
    def payment_id_validator(value):
        Validator._whole_number(value, "Payment id")

    @staticmethod
    def inventory_transaction_id_validator(value):
        Validator._whole_number(value, "Inventory transaction id")

    @staticmethod
    def delivery_id_validator(value):
        Validator._whole_number(value, "Delivery id")

    @staticmethod
    def bank_id_validator(value):
        Validator._whole_number(value, "Bank id")

# ---------- quantities and money ----------
    @staticmethod
    def quantity_validator(value):
        """Quantity of an order item or a stock movement: at least 1."""
        Validator._whole_number(value, "Quantity", minimum=1)

    @staticmethod
    def order_quantity_validator(value):
        """Total quantity of an order: an empty order has 0."""
        Validator._whole_number(value, "Quantity", minimum=0)

    @staticmethod
    def inventory_quantity_validator(value):
        Validator._whole_number(value, "Inventory quantity")

    @staticmethod
    def deficient_amount_validator(value):
        Validator._whole_number(value, "Deficient amount")

    @staticmethod
    def stock_inventory_validator(value):
        Validator._whole_number(value, "Stock")

    @staticmethod
    def price_validator(value):
        Validator._money(value, "Price", allow_zero=False)

    @staticmethod
    def total_price_validator(value):
        Validator._money(value, "Total price", allow_zero=True)

# ---------- texts ----------
    @staticmethod
    def product_name_validator(value):
        Validator._text(value, "Product name")

    @staticmethod
    def product_brand_validator(value):
        Validator._text(value, "Product brand")

    @staticmethod
    def customer_name_validator(value):
        # in orders and order items this is "name + family", so the limit is bigger
        Validator._text(value, "Customer name", 100)

    @staticmethod
    def person_name_validator(value, label="Name"):
        Validator._text(value, label, 50)

    @staticmethod
    def phone_validator(value):
        Validator._text(value, "Phone", 20)
        digits = [c for c in value if c.isdigit()]
        allowed = set("0123456789+-() ")
        if len(digits) < 7 or len(digits) > 15 or not set(value) <= allowed:
            raise ValueError("Phone must contain 7 to 15 digits")

    @staticmethod
    def address_validator(value):
        Validator._text(value, "Address", 200)

    @staticmethod
    def bank_name_validator(value):
        Validator._text(value, "Bank name", 50)

    @staticmethod
    def branch_code_validator(value):
        Validator._text(value, "Branch code", 20)

    @staticmethod
    def card_number_validator(value):
        digits = str(value).replace(" ", "").replace("-", "")
        if not digits.isdigit() or not 12 <= len(digits) <= 19:
            raise ValueError("Card number must contain 12 to 19 digits")

# ---------- choices ----------
    @staticmethod
    def order_type_validator(value):
        Validator._choice(value, "Order type", Validator.ORDER_TYPES)

    @staticmethod
    def status_validator(value):
        Validator._choice(value, "Status", Validator.ORDER_STATUSES)

    @staticmethod
    def inventory_transaction_type_validator(value):
        Validator._choice(value, "Transaction type", Validator.TRANSACTION_TYPES)

    @staticmethod
    def delivery_status_validator(value):
        Validator._choice(value, "Delivery status", Validator.DELIVERY_STATUSES)

# ---------- dates ----------
    @staticmethod
    def date_time_validator(value):
        Validator._date_text(value, "Date time")

    @staticmethod
    def order_time_validator(value):
        Validator._date_text(value, "Order time")

    @staticmethod
    def inventory_transaction_datetime_validator(value):
        Validator._date_text(value, "Transaction date time")

    @staticmethod
    def optional_date_validator(value):
        """Used for shipped/delivered times that may still be empty."""
        if value != "":
            Validator._date_text(value, "Date time")
