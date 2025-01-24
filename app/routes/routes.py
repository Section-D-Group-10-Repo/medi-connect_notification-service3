from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource, fields
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from app.models.models import Notification  # Import your Notification model

# Define the Blueprint
main_bp = Blueprint('main', __name__)

# Initialize Flask-RestX API
api = Api(main_bp, version='1.0', title='Notification Service API',
          description='A simple Notification Service API')

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

# Model for Swagger documentation
notification_model = api.model('Notification', {
    'id': fields.Integer(readOnly=True, description='The notification unique identifier'),
    'patient_id': fields.String(required=True, description='The patient ID associated with the notification'),
    'doctor_id': fields.String(required=True, description='The doctor ID associated with the notification'),
    'phone_number': fields.String(required=True, description='The phone number associated with the notification'),
    'message': fields.String(required=True, description='The message content of the notification'),
    'type': fields.String(required=True, description='The type of notification'),
    'read': fields.Boolean(required=True, description='The read status of the notification')
})

# Get all notifications
@api.route('/all-notifications')
class NotificationList(Resource):
    @api.marshal_list_with(notification_model)
    def get(self):
        """
        Fetch all notifications from the database.
        """
        db = SessionLocal()
        try:
            notifications = db.query(Notification).all()
            return notifications
        finally:
            db.close()

# Fetch notifications for a specific patient
@api.route('/patient/<string:patient_id>')
class PatientNotificationList(Resource):
    @api.marshal_list_with(notification_model)
    def get(self, patient_id):
        """
        Fetch notifications for a specific patient from the database.
        """
        db = SessionLocal()
        try:
            notifications = db.query(Notification).filter(Notification.patient_id == patient_id).all()
            return notifications
        finally:
            db.close()

# Fetch notifications for a specific doctor
@api.route('/doctor/<string:doctor_id>')
class DoctorNotificationList(Resource):
    @api.marshal_list_with(notification_model)
    def get(self, doctor_id):
        """
        Fetch notifications for a specific doctor from the database.
        """
        db = SessionLocal()
        try:
            notifications = db.query(Notification).filter(Notification.doctor_id == doctor_id).all()
            return notifications
        finally:
            db.close()

# Update read status of a notification
@api.route('/<int:notification_id>')
class NotificationResource(Resource):
    @api.expect(notification_model)
    @api.marshal_with(notification_model)
    def patch(self, notification_id):
        """
        Update read status of a notification in the database.
        """
        data = request.get_json()
        read_status = data.get('read')

        if read_status is None:
            return {"error": 'The "read" field is required.'}, 400

        db = SessionLocal()
        try:
            notification = db.query(Notification).filter(Notification.id == notification_id).first()
            if not notification:
                return {"error": "Notification not found"}, 404

            # Update the read status
            notification.read = read_status
            db.commit()

            return notification, 200
        finally:
            db.close()