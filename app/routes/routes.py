from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session, sessionmaker  # Import sessionmaker
from sqlalchemy import create_engine
from app.models.models import Notification  # Import your Notification model

# Define the Blueprint
main_bp = Blueprint('main', __name__)

# SQLite database file
DATABASE_URI = "sqlite:///notifications.db"

# Initialize SQLAlchemy engine
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Create and return a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home route
@main_bp.route('/')
def home():
    """
    Home route for the application.
    """
    return jsonify({"message": "Welcome to the Notification Service!"})

# Get all notifications
@main_bp.route('/all-notifications', methods=['GET'])
def get_notifications():
    """
    Route to fetch all notifications from the database.
    """
    db = SessionLocal()
    try:
        notifications = db.query(Notification).all()
        return jsonify([{
            "id": notification.id,
            "patient_id": notification.patient_id,
            "doctor_id": notification.doctor_id,
            "phone_number": notification.phone_number,
            "message": notification.message,
            "type": notification.type,
            "read": notification.read  # Include read status if it exists
        } for notification in notifications])
    finally:
        db.close()

# Fetch notifications for a specific patient
@main_bp.route('/patient/<string:patient_id>', methods=['GET'])
def get_notifications_by_patient(patient_id):
    """
    Fetch notifications for a specific patient from the database.
    """
    db = SessionLocal()
    try:
        notifications = db.query(Notification).filter(Notification.patient_id == patient_id).all()
        return jsonify([{
            "id": notification.id,
            "patient_id": notification.patient_id,
            "doctor_id": notification.doctor_id,
            "phone_number": notification.phone_number,
            "message": notification.message,
            "type": notification.type,
            "read": notification.read  # Include read status if it exists
        } for notification in notifications])
    finally:
        db.close()

# Fetch notifications for a specific doctor
@main_bp.route('/doctor/<string:doctor_id>', methods=['GET'])
def get_notifications_by_doctor(doctor_id):
    """
    Fetch notifications for a specific doctor from the database.
    """
    db = SessionLocal()
    try:
        notifications = db.query(Notification).filter(Notification.doctor_id == doctor_id).all()
        return jsonify([{
            "id": notification.id,
            "patient_id": notification.patient_id,
            "doctor_id": notification.doctor_id,
            "phone_number": notification.phone_number,
            "message": notification.message,
            "type": notification.type,
            "read": notification.read  # Include read status if it exists
        } for notification in notifications])
    finally:
        db.close()

# Update read status of a notification
@main_bp.route('/<int:notification_id>', methods=['PATCH'])
def mark_notification_as_read(notification_id):
    """
    Update read status of a notification in the database.
    """
    data = request.get_json()
    read_status = data.get('read')

    if read_status is None:
        return jsonify({"error": 'The "read" field is required.'}), 400

    db = SessionLocal()
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return jsonify({"error": "Notification not found"}), 404

        # Update the read status
        notification.read = read_status
        db.commit()

        return jsonify({
            "id": notification.id,
            "patient_id": notification.patient_id,
            "doctor_id": notification.doctor_id,
            "phone_number": notification.phone_number,
            "message": notification.message,
            "type": notification.type,
            "read": notification.read
        }), 200
    finally:
        db.close()