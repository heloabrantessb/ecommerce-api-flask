import os
from dotenv import load_dotenv

class Config:
    load_dotenv()

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ecommerce-flask-API.db'