import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///notifications.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RABBITMQ_URI = os.getenv('RABBITMQ_URI', 'localhost')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'notifications')
