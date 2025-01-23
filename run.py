from app import create_app, db
from app.consumer import start_consumer
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app instance
app = create_app()

def run_consumer():
    """
    Function to start the RabbitMQ consumer in a separate thread.
    Logs errors if the consumer fails.
    """
    try:
        logger.info("Starting RabbitMQ consumer...")
        start_consumer()
    except Exception as e:
        logger.error(f"Consumer error: {e}")

if __name__ == '__main__':
    # Start RabbitMQ consumer in a separate thread
    consumer_thread = threading.Thread(target=run_consumer)
    consumer_thread.daemon = True  # Ensures thread exits when main program ends
    consumer_thread.start()

    # Initialize the Flask app and database
    with app.app_context():
        try:
            logger.info("Initializing the database...")
            db.create_all()  # Create tables if they don't exist
            logger.info("Database initialized successfully.")
        except Exception as db_error:
            logger.error(f"Database initialization error: {db_error}")
            raise db_error

    # Start the Flask application
    try:
        logger.info("Starting the Flask application...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as app_error:
        logger.error(f"Flask application error: {app_error}")
