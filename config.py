import os

class Config:
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000
    SECRET_KEY = os.getenv('SECRET_KEY', 'api-escolar')
