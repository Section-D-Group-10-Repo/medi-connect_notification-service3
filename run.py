from app import create_app, db
from app.consumer import start_consumer
import threading

# Create Flask app instance
app = create_app()

def run_consumer():
    """
    Function to start the RabbitMQ consumer.
    """
    try:
        start_consumer()
    except Exception as e:
        # Log the error (use proper logging in production)
        print(f"Consumer error: {e}")

if __name__ == '__main__':
    # Start RabbitMQ consumer in a separate thread
    consumer_thread = threading.Thread(target=run_consumer)
    consumer_thread.daemon = True  # Ensures thread exits when main program ends
    consumer_thread.start()

    # Initialize the Flask app and database
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    # Start the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
