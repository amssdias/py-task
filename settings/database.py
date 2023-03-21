class Database(dict):
    
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self["users"] = []

    def clear(self):
        self["users"] = []


db_instance = Database()

if __name__ == "__main__":
    db = Database()
