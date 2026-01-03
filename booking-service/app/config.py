import os
from dotenv import load_dotenv

load_dotenv()

LOCK_SERVICE_URL = os.getenv("LOCK_SERVICE_URL")