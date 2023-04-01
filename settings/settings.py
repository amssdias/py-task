import string

string_characters = string.ascii_letters + string.digits + string.punctuation

# "".join(random.choice(string_characters) for _ in range(40))
SECRET_KEY = 'Y{\\1GFU&G-RKI81izq+:t4^155h;GcFUq|.%S?/B'

DATABASE_PATH = "data.db"
TEST_DATABASE_PATH = ":memory:"
