from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """
    Application factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    from app.routes.routes import main_bp  # Import your blueprint here
    app.register_blueprint(main_bp)

    return app
