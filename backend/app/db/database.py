import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_PASSWORD = quote_plus(os.getenv("DATABASE_PASSWORD"))

DATABASE_URL = (
    f"postgresql://{os.getenv('DATABASE_USER')}:"
    f"{DATABASE_PASSWORD}@"
    f"{os.getenv('DATABASE_HOST')}:"
    f"{os.getenv('DATABASE_PORT')}/"
    f"{os.getenv('DATABASE_NAME')}"
)

engine = create_engine(DATABASE_URL)