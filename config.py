import os

from dotenv import load_dotenv

from jwt_tools import ensure_jwt_secret

class Config:
    def __init__(self):
        load_dotenv()
        self.SECRET_KEY = ensure_jwt_secret()
        self.ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
        self.ADMIN_HASHED_PASSWORD = os.getenv('ADMIN_HASHED_PASSWORD')