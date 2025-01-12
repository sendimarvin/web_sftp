import os
from dotenv import load_dotenv

# Load environment variables from a .env file (optional)
load_dotenv()

class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{os.getenv('SQL_SERVER_USERNAME')}:{os.getenv('SQL_SERVER_PASSWORD')}"
        f"@{os.getenv('SQL_SERVER_HOST')}/{os.getenv('SQL_SERVER_DATABASE')}"
        f"?driver=ODBC+Driver+17+for+SQL+Server"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    BASE_DIR = os.getenv("BASE_DIR", "D:")
    #BASE_URL = os.getenv("BASE_URL", "/files")