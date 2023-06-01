import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", '1234asdf')


# Database configurations
DATABASE_PATH = "data.db"
TEST_DATABASE_PATH = "test.db"

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# Email settings
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
