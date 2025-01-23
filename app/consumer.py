import sys
import os
import pika
import json
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.models import Notification  # Import your Notification model

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# SQLite database file
DATABASE_URI = "sqlite:///notifications.db"

# Initialize SQLAlchemy engine
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_db():
    """
    Initialize the database and create tables if they don't exist.
    """
    try:
        # Import the Base class from your models (if you have one)
        from app.models.models import Base
        Base.metadata.create_all(bind=engine)
        logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")

def save_notification(data):
    """
    Save a notification to the database using SQLAlchemy.
    """
    try:
        logging.info("Saving notification to the database...")

        # Create a new session
        db = SessionLocal()

        # Create a new Notification object
        notification = Notification(
            patient_id=data.get('patient_id'),
            doctor_id=data.get('doctor_id'),
            phone_number=data.get('phone_number'),
            message=data['message'],
            type=data['type']
        )

        # Add and commit the notification to the database
        db.add(notification)
        db.commit()
        db.refresh(notification)

        logging.info("Notification saved to the database successfully")
        return notification
    except Exception as e:
        logging.error(f"Failed to save notification to the database: {e}")
        return None
    finally:
        db.close()

def process_message(ch, method, properties, body):
    """
    Process a message from RabbitMQ and save it to the database.
    """
    try:
        logging.info(f"Message received")
        data = json.loads(body)
        logging.info("Processing message...")

        # Extract the operation header
        operation = properties.headers.get('operation') if properties.headers else None

        if operation == "notify patient":
            # Send notification to the patient
            patient_id = data.get('patient_id')
            if not patient_id:
                logging.error("Patient ID is required for 'notify patient' operation")
                ch.basic_nack(delivery_tag=method.delivery_tag)
                return

            logging.info(f"Sending notification to patient: {patient_id}")
            # Here you can add logic to send the notification to the patient (e.g., via SMS, email, etc.)
            # For now, we'll just log it.
            logging.info(f"Notification for patient {patient_id}: {data['message']}")

        elif operation == "notify doctor":
            # Send notification to the doctor
            doctor_id = data.get('doctor_id')
            if not doctor_id:
                logging.error("Doctor ID is required for 'notify doctor' operation")
                ch.basic_nack(delivery_tag=method.delivery_tag)
                return

            logging.info(f"Sending notification to doctor: {doctor_id}")
            # Here you can add logic to send the notification to the doctor (e.g., via SMS, email, etc.)
            # For now, we'll just log it.
            logging.info(f"Notification for doctor {doctor_id}: {data['message']}")

        else:
            logging.error(f"Invalid operation: {operation}")
            ch.basic_nack(delivery_tag=method.delivery_tag)
            return

        # Save notification to the database
        notification = save_notification(data)
        if notification:
            logging.info(f"Successfully saved notification")

        # Acknowledge the message to RabbitMQ
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_consumer():
    """
    Start the RabbitMQ consumer to listen to the RPC-QUEUE.
    """
    try:
        # Initialize the database
        initialize_db()

        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the same queue as in the producer
        channel.queue_declare(queue='RPC-QUEUE')

        # Set up consumer
        channel.basic_consume(
            queue='RPC-QUEUE',
            on_message_callback=process_message
        )

        logging.info("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        logging.error(f"Error starting the consumer: {e}")

if __name__ == "__main__":
    start_consumer()