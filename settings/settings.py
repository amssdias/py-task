import random
import string

string_characters = string.ascii_letters + string.digits + string.punctuation

SECRET_KEY = "".join(random.choice(string_characters) for _ in range(15))
