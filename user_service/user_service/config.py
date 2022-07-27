import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    """
    toget secret code; goto terminal type python3
    import secrets
    secrets.token_urlsafe(16)
    """
    SECRET_KEY = 'BWex3nMlCab27thIaBkdnQ'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Praveen@localhost/student'
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    pass
