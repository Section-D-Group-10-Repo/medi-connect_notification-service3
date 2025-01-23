import os

class Config:
    """
    Application configuration class.
    Reads settings from environment variables with sensible defaults.
    """
    # General Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Make sure to set this in your environment or .env file
    DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Convert from string to boolean

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///notifications.db')  # Use an environment variable for the database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking for better performance

    # RabbitMQ Configuration
    RABBITMQ_URI = os.getenv('RABBITMQ_URI', 'localhost')  # RabbitMQ server URI
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'notifications')  # RabbitMQ queue name

    # Email Configuration
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')  # Default to Gmail
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))  # SMTP port (default is 587 for TLS)
    EMAIL_USER = os.getenv('EMAIL_USER', 'your_email@gmail.com')  # Sender email address
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your_password')  # Email account password

    # Additional configurations if needed
    # Example: Enable the usage of CSRF protection for forms (optional)
    # CSRF_ENABLED = True
