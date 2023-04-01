from settings.database.utils import create_tables_database
from settings.main_controller import MainController


if __name__ == "__main__":
    create_tables_database()
    try:
        app = MainController()
        app.start_app()
        
    except KeyboardInterrupt:
        print("Goodbye!")
