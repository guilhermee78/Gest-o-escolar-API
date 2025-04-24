import os

class Config:
    HOST = '0.0.0.0'
    PORT = 5001 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///escola.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
