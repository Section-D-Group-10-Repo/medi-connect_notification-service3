import pika
import json
from app import db
from app.models.models import Notification
from app.config import Config

def callback(ch, method, properties, body):
    """
    Callback to process messages from RabbitMQ.
    """
    try:
        message = json.loads(body)
        notification = Notification(
            patient_id=message.get('patient_id'),
            doctor_id=message.get('doctor_id'),
            message=message['message'],
            type=message['type']
        )
        db.session.add(notification)
        db.session.commit()
        print(f"Notification saved: {notification}")
    except Exception as e:
        print(f"Error processing message: {e}")

def start_consumer():
    """
    Starts the RabbitMQ consumer.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(Config.RABBITMQ_URI))
    channel = connection.channel()
    channel.queue_declare(queue=Config.RABBITMQ_QUEUE)

    print("Waiting for messages. To exit press CTRL+C")
    channel.basic_consume(
        queue=Config.RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=True
    )
    channel.start_consuming()
