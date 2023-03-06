from settings.main_controller import MainController


if __name__ == "__main__":

    try:
        app = MainController()
        app.start_app()
        
    except KeyboardInterrupt:
        print("Goodbye!")
