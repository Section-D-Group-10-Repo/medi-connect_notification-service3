from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()  # Adding Flask-Migrate for database migrations

def create_app():
    """
    Factory function to create the Flask application.
    Configures the app and initializes extensions.
    """
    app = Flask(__name__)
    
    # Load configuration from the Config class
    app.config.from_object('app.config.Config')  # This loads from the environment variables or defaults

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db

    # Register blueprints
    from app.routes.routes import main_bp  # Ensure routes are correctly imported
    app.register_blueprint(main_bp)

    # Additional debugging route (optional)
    @app.route('/ping')
    def ping():
        return "Pong!", 200  # Simple route to check the server status

    return app