from dotenv import load_dotenv
import os

load_dotenv()
DB_NAME = os.environ.get("DB_NAME")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PATH_HOSTED = os.environ.get("DB_PATH_HOSTED")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
API_AUDIENCE = os.environ.get("API_AUDIENCE")