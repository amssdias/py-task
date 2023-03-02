class Database(dict):
    
    def __init__(self):
        self["users"] = []


if __name__ == "__main__":
    db = Database()