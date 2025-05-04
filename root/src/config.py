import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"

    # More here if needed in development
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables a feature we don't need

    SECRET_KEY = "test" #  Secret key for Flask sessions (required for login, cookies, etc.)