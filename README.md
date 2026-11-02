# Store Management System (team project)

A small desktop application (Python, tkinter, SQLite) to manage customers, products, stock,
orders, payments and deliveries.

## How to run

```
python main.py          # starts the program (the database is created automatically)
python -m unittest discover -s tests -t . -p "*test*.py"     # runs the tests
pytest                  # same tests, if pytest is installed (pip install -r requirements.txt)
```
tkinter and sqlite3 come with Python, no other package is needed to run the program.
The database file is created in `data/store.db`.

## Project structure

| Folder | Content |
|---|---|
| `models/` | Classes of the data (Customer, Product, Inventory, Inventory_Transaction, Order, Order_Item, PaymentTransaction, Bank, Delivery) with validation in the setters |
| `tools/` | `validation.py` (Validator: all checks) and `helpers.py` (date/time text) |
| `database/` | `schema.sql` (tables), `connection.py` (connection + transaction), `init_db.py` |
| `repositories/` | SQL only: save / find / delete of every model |
| `services/` | Business rules (stock check, order status, payment rules, ...) |
| `controller/` | Connects a screen with a service; returns `(success, message)` |
| `ui/` | `main_window.py` (menu) and `views/` (one tkinter screen per topic) |
| `tests/` | Unit tests |

Flow of a request: **view -> controller -> service -> repository -> database**.

## How the program works

1. **Customers / Products**: create them. A new product gets an inventory row with its first stock.
2. **Orders**: create an order (`sell`, `buy` or `cart`) for a customer, then use **Items** to add products.
   Total price and quantity are calculated from the items.
3. **Complete** an order: a sell order reduces the stock, a buy order increases it
   (every change is written as an inventory transaction). **Cancel** a completed sell order gives the stock back.
4. **Payments**: only a completed order can be paid, once. For a sell order the card number is checked
   and only the last 4 digits are saved.
5. **Deliveries**: for a completed sell order. It must be paid before it is shipped:
   pending -> shipped -> delivered.
6. **Inventory** screen shows the stock (low stock is red) and lets you change the low-stock limit.
   **Inventory Transactions** screen adds or removes stock by hand.

## Fixes made in `models/` (no design change, only debugging)

- `customer.py`, `payment_transaction.py`: the demo code ran on every import (and asked for input). Now it runs only when the file is started directly. `payment_transaction.py` also imported `customer` the wrong way, `payer` was the class instead of a customer, `get_card_number` returned nothing, and the empty `total_amount` method was removed (the total comes from the order).
- `order.py`: `quantuty` typo; getter used `_order_id` / `__total_amount` names that did not exist; `@order_name.setter`; wrong `@customer_id.setter` on `inventory_transaction_id`; bad indentation; missing comma in `to_tuple`; `to_tuple` was a property; `order_time` used `date + minutes` (does nothing), now a real date/time text; removed the strange `from tests import ...` import.
- `order_item.py`: the `quantity` setter was named `price` (it replaced the price setter); bad indentation; broken `__repr__`; wrong import.
- `product.py`: `product_brand` was not a parameter and had a setter without a getter; `product_name` was written twice.
- `inventory.py`: `inventory_time` was the `time` class; `deficient_amount` property names had typos; the date/time parameters were ignored.
- `inventory_transaction.py`: class name typo (`Inventoryr_Tansaction` -> `Inventory_Transaction`); undefined `Inventory_Transaction_Id`; `@order_id` / `@product_id` used instead of `@property`.
- All models: `__repr__` was written in a way that raises an error, validator names did not exist (now all in `tools/validation.py`).
- `bank.py` and `delivery.py` were empty, they are written now in the same style.

## Notes

- Money is stored as a normal number (e.g. 2.5).
- `schema.sql` was changed to match the model classes (for example customers have name / family / phone).
