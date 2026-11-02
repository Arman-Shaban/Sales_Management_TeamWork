# Common code of all controllers.
# A controller sits between a view (screen) and a service. It converts the text typed in
# the screen to numbers, calls the service and returns  (success, message_or_data)
# so the view never has to deal with exceptions.
import sqlite3

from database.connection import DEFAULT_DB_PATH, Database
from services.errors import StoreError


class BaseController:
    def __init__(self, db=None):
        self.db = db or Database(DEFAULT_DB_PATH)

    @staticmethod
    def to_int(text, label):
        try:
            return int(str(text).strip())
        except ValueError:
            raise ValueError(f"{label} must be a whole number")

    @staticmethod
    def to_float(text, label):
        try:
            return float(str(text).strip())
        except ValueError:
            raise ValueError(f"{label} must be a number")

    @staticmethod
    def run(action, success_message):
        """Run action(); return (True, success_message) or (False, error text)."""
        try:
            action()
            return True, success_message
        except (ValueError, StoreError) as error:
            return False, str(error)
        except sqlite3.Error as error:
            return False, f"Database error: {error}"

    @staticmethod
    def load(action):
        """Run action() that returns a list; return (True, list) or (False, [])."""
        try:
            return True, action()
        except (ValueError, StoreError, sqlite3.Error):
            return False, []
