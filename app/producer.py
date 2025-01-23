import pika
import json
from utils import validate_phone_number, validate_email

def publish_message(patient_id, doctor_id, message, message_type, email, phone_number, operation):
    """
    Publishes a message to the RabbitMQ queue.
    Includes validation for email and phone number.
    """
    if not validate_email(email):
        print(f"Invalid email: {email}")
        return
    
    if not validate_phone_number(phone_number):
        print(f"Invalid phone number: {phone_number}")
        return

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare the queue for the consumer to listen to (use same name as consumer)
        channel.queue_declare(queue='RPC-QUEUE')

        # Message structure
        message_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "message": message,
            "type": message_type,
            "email": email,
            "phone_number": phone_number  # Added phone number
        }

        # Publish message to the queue with headers
        channel.basic_publish(
            exchange='',
            routing_key='RPC-QUEUE',
            body=json.dumps(message_data),
            properties=pika.BasicProperties(
                headers={'operation': operation}  # Add the operation header
            )
        )

        print(f"Message sent: {message_data}")
        connection.close()
    except Exception as e:
        print(f"Error sending message: {e}")

if __name__ == '__main__':
    # Example test call
    publish_message(
        patient_id="123",
        doctor_id="456",
        message="You have a new appointment.",
        message_type="alert",
        email="natnael.meseret.w@gmail.com",
        phone_number="+1234567890",
        operation="notify patient"  # Specify the operation
    )