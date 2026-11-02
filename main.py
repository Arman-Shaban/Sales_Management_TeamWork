# Start the program:  python main.py
from database.connection import DEFAULT_DB_PATH, Database
from database.init_db import initialize
from ui.main_window import MainWindow


def main():
    initialize(Database(DEFAULT_DB_PATH))     # creates the tables the first time
    MainWindow().run()


if __name__ == "__main__":
    main()
