import sys
import os
import pika
import json
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db, create_app
from app.models.models import Notification

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the Flask app and push the context
app = create_app()
app.app_context().push()

def save_notification(data):
    try:
        logging.info("Saving notification to the database...")
        notification = Notification(
            patient_id=data.get('patient_id'),
            doctor_id=data.get('doctor_id'),
            phone_number=data.get('phone_number'),  # Save the phone number
            message=data['message'],
            type=data['type']
        )
        db.session.add(notification)
        db.session.commit()
        logging.info(f"Notification saved")
        return notification
    except Exception as e:
        logging.error(f"Failed to save notification")
        return None

def process_message(ch, method, properties, body):
    try:
        logging.info(f"Message received")
        data = json.loads(body)
        logging.info("Processing message...")

        # Save notification to DB
        notification = save_notification(data)
        if notification:
            logging.info(f"Successfully saved notification")
        
        # Acknowledge the message to RabbitMQ
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_consumer():
    """
    Start the RabbitMQ consumer to listen to the RPC-QUEUE.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the same queue as in the producer
        channel.queue_declare(queue='RPC-QUEUE')

        # Set up consumer
        channel.basic_consume(
            queue='RPC-QUEUE',
            on_message_callback=process_message
        )

        channel.start_consuming()
    except Exception as e:
        print(f"Error starting the consumer")

if __name__ == "__main__":
    print("suuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
    start_consumer()
